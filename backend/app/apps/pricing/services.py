from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Iterable, List, Sequence

from app.apps.cars.models import Car
from app.apps.pricing.models import PricingRule


@dataclass(slots=True)
class PricingContext:
    car: Car
    start_date: date
    end_date: date

    @property
    def rental_days(self) -> int:
        return max(1, (self.end_date - self.start_date).days)


class PricingStrategy:
    name = "base"

    def apply(self, total: Decimal, context: PricingContext) -> tuple[Decimal, str]:
        raise NotImplementedError


class BasePriceStrategy(PricingStrategy):
    name = "base"

    def apply(self, total: Decimal, context: PricingContext) -> tuple[Decimal, str]:
        base = Decimal(context.rental_days) * context.car.base_price_per_day
        return base, f"Base price for {context.rental_days} day(s)"


class DurationDiscountStrategy(PricingStrategy):
    name = "duration"

    def __init__(self, thresholds: Sequence[dict[str, float]]) -> None:
        self.thresholds = sorted(thresholds, key=lambda x: x["days"], reverse=True)

    def apply(self, total: Decimal, context: PricingContext) -> tuple[Decimal, str]:
        discount = Decimal("0")
        applied = None
        for rule in self.thresholds:
            if context.rental_days >= int(rule["days"]):
                applied = rule
                discount = total * Decimal(rule.get("discount_pct", 0)) / Decimal("100") * Decimal("-1")
                break
        if applied:
            return discount, f"Duration discount {applied['discount_pct']}%"
        return Decimal("0"), "No duration discount"


class YearDepreciationStrategy(PricingStrategy):
    name = "year"

    def __init__(self, per_year_pct: float, max_pct: float) -> None:
        self.per_year_pct = Decimal(str(per_year_pct))
        self.max_pct = Decimal(str(max_pct))

    def apply(self, total: Decimal, context: PricingContext) -> tuple[Decimal, str]:
        current_year = date.today().year
        age = max(0, current_year - context.car.year)
        pct = min(self.per_year_pct * Decimal(age), self.max_pct)
        if pct <= 0:
            return Decimal("0"), "No age adjustment"
        discount = total * pct / Decimal("100") * Decimal("-1")
        return discount, f"Age discount {pct}%"


class SeasonalStrategy(PricingStrategy):
    name = "seasonal"

    def __init__(self, seasons: Sequence[dict[str, float]]) -> None:
        self.seasons = seasons

    def apply(self, total: Decimal, context: PricingContext) -> tuple[Decimal, str]:
        start = context.start_date
        for season in self.seasons:
            start_str = season.get("start")
            end_str = season.get("end")
            if not start_str or not end_str:
                continue
            start_month, start_day = map(int, start_str.split("-"))
            end_month, end_day = map(int, end_str.split("-"))
            start_tuple = (start_month, start_day)
            end_tuple = (end_month, end_day)
            if start_tuple <= (start.month, start.day) <= end_tuple:
                pct = Decimal(str(season.get("surcharge_pct", 0)))
                surcharge = total * pct / Decimal("100")
                return surcharge, f"Seasonal surcharge {pct}%"
        return Decimal("0"), "No seasonal adjustment"


class PricingService:
    """Strategy pattern implementation orchestrating pricing rules."""

    def __init__(self, rules: Iterable[PricingRule] | None = None) -> None:
        self.rules = list(rules) if rules is not None else list(PricingRule.objects.filter(is_active=True))

    def _build_strategies(self, context: PricingContext) -> List[PricingStrategy]:
        strategies: List[PricingStrategy] = [BasePriceStrategy()]
        duration_rules = [r for r in self.rules if r.strategy_type == PricingRule.StrategyType.DURATION]
        if duration_rules:
            thresholds: list[dict[str, float]] = []
            for rule in duration_rules:
                thresholds.extend(rule.params.get("thresholds", []))
            strategies.append(DurationDiscountStrategy(thresholds))
        year_rules = [r for r in self.rules if r.strategy_type == PricingRule.StrategyType.YEAR]
        if year_rules:
            params = year_rules[0].params
            strategies.append(
                YearDepreciationStrategy(
                    per_year_pct=params.get("per_year_pct", 0),
                    max_pct=params.get("max_pct", 50),
                )
            )
        seasonal_rules = [r for r in self.rules if r.strategy_type == PricingRule.StrategyType.SEASONAL]
        if seasonal_rules:
            seasons: list[dict[str, float]] = []
            for rule in seasonal_rules:
                seasons.extend(rule.params.get("seasons", []))
            strategies.append(SeasonalStrategy(seasons))
        return strategies

    def quote(self, car: Car, start_date: date, end_date: date) -> dict[str, object]:
        context = PricingContext(car=car, start_date=start_date, end_date=end_date)
        total = Decimal("0")
        breakdown: list[dict[str, object]] = []
        for strategy in self._build_strategies(context):
            delta, reason = strategy.apply(total if strategy.name != "base" else total, context)
            if strategy.name == "base":
                total = delta
            else:
                total += delta
            breakdown.append({"strategy": strategy.name, "delta": float(delta), "reason": reason})
        return {"total": float(total), "breakdown": breakdown}

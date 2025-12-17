from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Dict, Iterable, List

from apps.pricing.models import PricingRule


def to_decimal(value: Decimal | float | int | str) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass
class PricingContext:
    car: Any
    start_date: date
    end_date: date

    @property
    def rental_days(self) -> int:
        return max((self.end_date - self.start_date).days, 1)


@dataclass
class PriceBreakdownItem:
    name: str
    amount: Decimal
    metadata: Dict | None = None


@dataclass
class PricingResult:
    breakdown: List[PriceBreakdownItem] = field(default_factory=list)
    total: Decimal = field(default_factory=lambda: Decimal("0.00"))

    def add_item(self, name: str, amount: Decimal, metadata: Dict | None = None) -> None:
        normalized = to_decimal(amount)
        self.breakdown.append(PriceBreakdownItem(name=name, amount=normalized, metadata=metadata))
        self.total += normalized

    def as_dict(self) -> Dict:
        return {
            "total": to_decimal(self.total),
            "breakdown": [
                {
                    "name": item.name,
                    "amount": to_decimal(item.amount),
                    "metadata": item.metadata or {},
                }
                for item in self.breakdown
            ],
        }


class PricingStrategy:
    def apply(self, context: PricingContext, result: PricingResult) -> None:  # pragma: no cover - interface
        raise NotImplementedError


class BasePriceStrategy(PricingStrategy):
    label = "Base price"

    def apply(self, context: PricingContext, result: PricingResult) -> None:
        amount = to_decimal(context.car.base_price_per_day) * context.rental_days
        result.add_item(self.label, amount, metadata={"days": context.rental_days})


class DurationDiscountStrategy(PricingStrategy):
    label = "Duration discount"

    def __init__(self, rules: Iterable[PricingRule] | None = None) -> None:
        self.rules = list(rules) if rules else []

    def apply(self, context: PricingContext, result: PricingResult) -> None:
        rate = self._resolve_rate(context.rental_days)
        if rate <= 0:
            return
        discount = result.total * rate
        result.add_item(self.label, -discount, metadata={"rate": float(rate)})

    def _resolve_rate(self, rental_days: int) -> Decimal:
        matched_rate = Decimal("0.00")
        for rule in self.rules:
            params = rule.params or {}
            min_days = int(params.get("min_days", 0))
            if rental_days >= min_days:
                rule_rate = to_decimal(params.get("discount_rate", 0))
                matched_rate = max(matched_rate, rule_rate)
        if not self.rules and rental_days >= 7:
            matched_rate = Decimal("0.10")
        return matched_rate


class YearDepreciationStrategy(PricingStrategy):
    label = "Year depreciation"

    def __init__(self, rules: Iterable[PricingRule] | None = None) -> None:
        self.rules = list(rules) if rules else []

    def apply(self, context: PricingContext, result: PricingResult) -> None:
        depreciation_rate = self._resolve_rate(context.car.year)
        if depreciation_rate <= 0:
            return
        amount = result.total * depreciation_rate
        result.add_item(self.label, -amount, metadata={"rate": float(depreciation_rate)})

    def _resolve_rate(self, car_year: int) -> Decimal:
        if self.rules:
            params = self.rules[0].params or {}
            return to_decimal(params.get("rate", 0))

        current_year = date.today().year
        age = max(current_year - car_year, 0)
        return min(Decimal("0.01") * age, Decimal("0.20"))


class SeasonalStrategy(PricingStrategy):
    label = "Seasonal adjustment"

    def __init__(self, rules: Iterable[PricingRule] | None = None) -> None:
        self.rules = list(rules) if rules else []

    def apply(self, context: PricingContext, result: PricingResult) -> None:
        month = context.start_date.month
        applicable_rules = self.rules or PricingRule.objects.filter(
            strategy_type=PricingRule.StrategyType.SEASONAL, active=True
        )
        for rule in applicable_rules:
            params = rule.params or {}
            months = params.get("months", [])
            if month not in months:
                continue
            multiplier = to_decimal(params.get("multiplier", 1))
            adjustment = result.total * (multiplier - 1)
            if adjustment == 0:
                continue
            result.add_item(rule.name or self.label, adjustment, metadata={"multiplier": float(multiplier)})

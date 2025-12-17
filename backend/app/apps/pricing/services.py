from datetime import date
from typing import Iterable, Sequence

from apps.pricing.models import PricingRule

from .strategies import (
    BasePriceStrategy,
    DurationDiscountStrategy,
    PricingContext,
    PricingResult,
    SeasonalStrategy,
    YearDepreciationStrategy,
)


class PricingService:
    def __init__(self, strategies: Sequence | None = None) -> None:
        self.strategies = list(strategies) if strategies else self._default_strategies()

    def _default_strategies(self) -> Iterable:
        seasonal_rules = PricingRule.objects.filter(
            strategy_type=PricingRule.StrategyType.SEASONAL, active=True
        )
        duration_rules = PricingRule.objects.filter(
            strategy_type=PricingRule.StrategyType.DURATION_DISCOUNT, active=True
        )
        depreciation_rules = PricingRule.objects.filter(
            strategy_type=PricingRule.StrategyType.YEAR_DEPRECIATION, active=True
        )
        return (
            BasePriceStrategy(),
            DurationDiscountStrategy(duration_rules),
            YearDepreciationStrategy(depreciation_rules),
            SeasonalStrategy(seasonal_rules),
        )

    def quote(self, car, start_date: date, end_date: date) -> dict:
        if end_date <= start_date:
            raise ValueError("End date must be after start date")

        context = PricingContext(car=car, start_date=start_date, end_date=end_date)
        result = PricingResult()
        for strategy in self.strategies:
            strategy.apply(context, result)
        return result.as_dict()

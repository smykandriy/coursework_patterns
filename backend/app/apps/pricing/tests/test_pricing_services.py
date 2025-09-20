from datetime import date

import pytest

from app.apps.cars.models import Car
from app.apps.pricing.models import PricingRule
from app.apps.pricing.services import PricingService


@pytest.mark.django_db
def test_pricing_pipeline_applies_strategies():
    car = Car.objects.create(
        make="Tesla",
        model="Model 3",
        year=2020,
        vin="VIN123",
        type="sedan",
        base_price_per_day=100,
        status=Car.Status.AVAILABLE,
        mileage=10000,
    )
    PricingRule.objects.create(
        name="Weekly discount",
        strategy_type=PricingRule.StrategyType.DURATION,
        params={"thresholds": [{"days": 7, "discount_pct": 10}]},
    )
    PricingRule.objects.create(
        name="Depreciation",
        strategy_type=PricingRule.StrategyType.YEAR,
        params={"per_year_pct": 2, "max_pct": 20},
    )
    PricingRule.objects.create(
        name="Summer surge",
        strategy_type=PricingRule.StrategyType.SEASONAL,
        params={"seasons": [{"start": "06-01", "end": "08-31", "surcharge_pct": 5}]},
    )

    service = PricingService()
    quote = service.quote(car, date(2025, 6, 1), date(2025, 6, 8))

    assert quote["total"] > 0
    strategies = {entry["strategy"] for entry in quote["breakdown"]}
    assert {"base", "duration", "year", "seasonal"}.issubset(strategies)

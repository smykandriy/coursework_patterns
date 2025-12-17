from datetime import date, timedelta
from decimal import Decimal

import pytest

from apps.pricing.models import PricingRule
from apps.pricing.services import PricingService


@pytest.mark.django_db
def test_pricing_breakdown_total_with_seasonal(car):
    PricingRule.objects.create(
        name="Summer uplift",
        strategy_type=PricingRule.StrategyType.SEASONAL,
        params={"months": [7], "multiplier": 1.2},
        active=True,
    )

    service = PricingService()
    start = date(2025, 7, 1)
    end = start + timedelta(days=3)

    quote = service.quote(car, start, end)

    assert quote["total"] == Decimal("360.00")
    assert sum(item["amount"] for item in quote["breakdown"]) == Decimal("360.00")
    assert {item["name"] for item in quote["breakdown"]} == {"Base price", "Summer uplift"}

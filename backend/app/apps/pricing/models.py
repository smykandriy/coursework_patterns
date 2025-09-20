from __future__ import annotations

from django.db import models

from app.apps.common.models import TimeStampedModel


class PricingRule(TimeStampedModel):
    class StrategyType(models.TextChoices):
        DURATION = "duration", "Duration discount"
        YEAR = "year", "Year depreciation"
        SEASONAL = "seasonal", "Seasonal adjustment"

    name = models.CharField(max_length=120)
    strategy_type = models.CharField(max_length=20, choices=StrategyType.choices)
    params = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

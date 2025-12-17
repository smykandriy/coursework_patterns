from uuid import uuid4

from django.db import models


class PricingRule(models.Model):
    class StrategyType(models.TextChoices):
        SEASONAL = "seasonal", "Seasonal"
        DURATION_DISCOUNT = "duration_discount", "Duration Discount"
        YEAR_DEPRECIATION = "year_depreciation", "Year Depreciation"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=128)
    strategy_type = models.CharField(max_length=64, choices=StrategyType.choices)
    params = models.JSONField(default=dict)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - display utility
        return f"{self.name} ({self.strategy_type})"

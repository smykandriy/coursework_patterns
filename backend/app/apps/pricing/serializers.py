from __future__ import annotations

from rest_framework import serializers

from app.apps.pricing.models import PricingRule


class PricingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingRule
        fields = ["id", "name", "strategy_type", "params", "is_active"]


class PricingQuoteRequestSerializer(serializers.Serializer):
    car = serializers.UUIDField()
    start = serializers.DateField()
    end = serializers.DateField()

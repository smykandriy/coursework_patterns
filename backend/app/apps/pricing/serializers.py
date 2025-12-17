from rest_framework import serializers

from .models import PricingRule


class PricingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingRule
        fields = ["id", "name", "strategy_type", "params", "active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

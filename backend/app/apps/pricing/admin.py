from django.contrib import admin

from app.apps.pricing.models import PricingRule


@admin.register(PricingRule)
class PricingRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "strategy_type", "is_active")
    list_filter = ("strategy_type", "is_active")

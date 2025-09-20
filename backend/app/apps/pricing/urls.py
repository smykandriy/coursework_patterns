from __future__ import annotations

from django.urls import path
from rest_framework.routers import DefaultRouter

from app.apps.pricing.views import PricingQuoteView, PricingRuleViewSet

router = DefaultRouter()
router.register(r"pricing/rules", PricingRuleViewSet, basename="pricing-rule")

urlpatterns = [
    path("pricing/quote/", PricingQuoteView.as_view(), name="pricing-quote"),
]
urlpatterns += router.urls

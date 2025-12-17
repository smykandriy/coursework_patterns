from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PricingRuleViewSet, QuoteView

router = DefaultRouter()
router.register("rules", PricingRuleViewSet, basename="pricing-rule")

urlpatterns = [
    path("quote/", QuoteView.as_view(), name="pricing-quote"),
]

urlpatterns += router.urls

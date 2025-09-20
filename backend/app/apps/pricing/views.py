from __future__ import annotations

from rest_framework import permissions, response, status, viewsets
from rest_framework.views import APIView

from app.apps.cars.models import Car
from app.apps.pricing.models import PricingRule
from app.apps.pricing.serializers import (
    PricingQuoteRequestSerializer,
    PricingRuleSerializer,
)
from app.apps.pricing.services import PricingService


class PricingQuoteView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = PricingQuoteRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        car = Car.objects.get(id=serializer.validated_data["car"])
        service = PricingService()
        quote = service.quote(car, serializer.validated_data["start"], serializer.validated_data["end"])
        return response.Response(quote)


class PricingRuleViewSet(viewsets.ModelViewSet):
    queryset = PricingRule.objects.all()
    serializer_class = PricingRuleSerializer
    permission_classes = [permissions.IsAdminUser]

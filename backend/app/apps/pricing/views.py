from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cars.models import Car
from apps.common.permissions import IsAdmin
from apps.pricing.services import PricingService

from .models import PricingRule
from .serializers import PricingRuleSerializer


class QuoteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        car_id = request.query_params.get("car")
        start = request.query_params.get("start")
        end = request.query_params.get("end")
        if not (car_id and start and end):
            return Response(
                {"detail": "car, start, and end query parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"detail": "Invalid date format, expected YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        car = get_object_or_404(Car, id=car_id)
        try:
            quote = PricingService().quote(car, start_date, end_date)
        except ValueError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(quote)


class PricingRuleViewSet(viewsets.ModelViewSet):
    queryset = PricingRule.objects.all()
    serializer_class = PricingRuleSerializer
    permission_classes = [IsAdmin]

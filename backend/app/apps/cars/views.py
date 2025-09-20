from __future__ import annotations

from rest_framework import permissions, viewsets

from app.apps.cars.models import Car
from app.apps.cars.serializers import CarSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = {
        "type": ["exact"],
        "year": ["gte", "lte"],
        "base_price_per_day": ["lte"],
        "status": ["exact"],
    }
    ordering = ["make", "model"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        user = self.request.user
        if user.is_authenticated and user.role in {"admin", "manager"}:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

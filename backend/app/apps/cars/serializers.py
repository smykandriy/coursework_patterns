from __future__ import annotations

from rest_framework import serializers

from app.apps.cars.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = [
            "id",
            "make",
            "model",
            "year",
            "vin",
            "type",
            "base_price_per_day",
            "status",
            "mileage",
            "last_service_at",
        ]

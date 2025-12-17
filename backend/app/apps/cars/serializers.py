from rest_framework import serializers

from .models import Car


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
        read_only_fields = ["id"]

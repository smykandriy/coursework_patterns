from rest_framework import serializers

from apps.cars.serializers import CarSerializer
from apps.cars.models import Car

from .models import Booking, Deposit, Fine, Invoice


class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = ["id", "type", "amount", "notes", "assessed_at"]
        read_only_fields = ["id", "assessed_at"]


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ["id", "amount", "status", "txn_ref", "created_at", "updated_at"]
        read_only_fields = ["id", "status", "txn_ref", "created_at", "updated_at"]


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "id",
            "breakdown",
            "total",
            "paid_at",
            "method",
            "payment_reference",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "breakdown",
            "total",
            "paid_at",
            "method",
            "payment_reference",
            "created_at",
            "updated_at",
        ]


class BookingSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(
        source="car", queryset=Car.objects.all(), write_only=True
    )
    fines = FineSerializer(many=True, read_only=True)
    deposit = DepositSerializer(read_only=True)
    invoice = InvoiceSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "customer",
            "car",
            "car_id",
            "start_date",
            "end_date",
            "status",
            "created_at",
            "updated_at",
            "fines",
            "deposit",
            "invoice",
        ]
        read_only_fields = ["id", "customer", "status", "created_at", "updated_at", "car"]

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError("End date must be after start date.")
        return attrs

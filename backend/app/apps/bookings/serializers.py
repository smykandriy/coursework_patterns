from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from app.apps.bookings.models import Booking, Deposit, Fine, Invoice
from app.apps.cars.serializers import CarSerializer
from app.apps.users.serializers import UserSerializer


class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = ["id", "type", "amount", "notes", "resolved_at"]


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ["amount", "status", "txn_ref", "updated_at"]


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "amount_rental",
            "amount_fees",
            "amount_fines",
            "amount_total",
            "paid_at",
            "method",
        ]


class BookingSerializer(serializers.ModelSerializer):
    car = CarSerializer(read_only=True)
    customer = UserSerializer(source="customer.user", read_only=True)
    deposit = DepositSerializer(read_only=True)
    invoice = InvoiceSerializer(read_only=True)
    fines = FineSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "customer",
            "car",
            "start_date",
            "end_date",
            "status",
            "notes",
            "deposit",
            "invoice",
            "fines",
        ]


class BookingCreateSerializer(serializers.Serializer):
    car_id = serializers.UUIDField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    notes = serializers.CharField(allow_blank=True, required=False)


class BookingActionSerializer(serializers.Serializer):
    booking_id = serializers.UUIDField()


class BookingReturnSerializer(serializers.Serializer):
    mileage_delta = serializers.IntegerField()
    fines = FineSerializer(many=True, required=False)

    def validate_fines(self, fines):
        return fines or []

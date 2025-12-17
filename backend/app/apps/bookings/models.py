from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.cars.models import Car


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        CANCELED = "canceled", "Canceled"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings"
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date", "car"]
        indexes = [models.Index(fields=["car", "start_date", "end_date"])]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gt=models.F("start_date")),
                name="booking_end_after_start",
            ),
        ]

    def __str__(self) -> str:  # pragma: no cover - display utility
        return f"Booking {self.id} for {self.car}"


class Deposit(models.Model):
    class Status(models.TextChoices):
        HELD = "held", "Held"
        RELEASED = "released", "Released"
        PARTIALLY_RELEASED = "partially_released", "Partially Released"
        FORFEITED = "forfeited", "Forfeited"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="deposit")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=24, choices=Status.choices, default=Status.HELD)
    txn_ref = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # pragma: no cover - display utility
        return f"Deposit for {self.booking_id} ({self.status})"


class Fine(models.Model):
    class FineType(models.TextChoices):
        DAMAGE = "damage", "Damage"
        LATE_RETURN = "late_return", "Late Return"
        CLEANING = "cleaning", "Cleaning"
        OTHER = "other", "Other"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="fines")
    type = models.CharField(max_length=20, choices=FineType.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    assessed_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:  # pragma: no cover - display utility
        return f"{self.get_type_display()} fine for booking {self.booking_id}"


class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="invoice")
    breakdown = models.JSONField(default=list)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(null=True, blank=True)
    method = models.CharField(max_length=64, blank=True)
    payment_reference = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # pragma: no cover - display utility
        return f"Invoice for booking {self.booking_id}"

from __future__ import annotations

from datetime import date

from django.db import models
from django.utils import timezone

from app.apps.cars.models import Car
from app.apps.common.models import TimeStampedModel
from app.apps.users.models import Customer


class BookingQuerySet(models.QuerySet):
    def active(self) -> "BookingQuerySet":
        return self.filter(status__in=[Booking.Status.CONFIRMED, Booking.Status.ACTIVE])

    def for_period(self, start: date, end: date) -> "BookingQuerySet":
        return self.filter(start_date__lt=end, end_date__gt=start)


class Booking(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        CANCELED = "canceled", "Canceled"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="bookings")
    car = models.ForeignKey(Car, on_delete=models.PROTECT, related_name="bookings")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)

    objects = BookingQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(check=models.Q(end_date__gt=models.F("start_date")), name="booking_valid_dates"),
        ]
        indexes = [
            models.Index(fields=["car", "start_date", "end_date"]),
        ]

    def overlaps(self, start: date, end: date) -> bool:
        return not (self.end_date <= start or self.start_date >= end)

    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days


class Deposit(TimeStampedModel):
    class Status(models.TextChoices):
        HELD = "held", "Held"
        RELEASED = "released", "Released"
        PARTIALLY_RELEASED = "partially_released", "Partially released"
        FORFEITED = "forfeited", "Forfeited"

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="deposit")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.HELD)
    txn_ref = models.CharField(max_length=64, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class Fine(TimeStampedModel):
    class Type(models.TextChoices):
        DAMAGE = "damage", "Damage"
        LATE_RETURN = "late_return", "Late return"
        CLEANING = "cleaning", "Cleaning"
        OTHER = "other", "Other"

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="fines")
    type = models.CharField(max_length=20, choices=Type.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.CharField(max_length=255, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)


class Invoice(TimeStampedModel):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="invoice")
    amount_rental = models.DecimalField(max_digits=10, decimal_places=2)
    amount_fees = models.DecimalField(max_digits=10, decimal_places=2)
    amount_fines = models.DecimalField(max_digits=10, decimal_places=2)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(null=True, blank=True)
    method = models.CharField(max_length=50, blank=True)

    def mark_paid(self, method: str) -> None:
        self.method = method
        self.paid_at = timezone.now()
        self.save(update_fields=["method", "paid_at"])

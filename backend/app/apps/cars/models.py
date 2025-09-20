from __future__ import annotations

from django.db import models

from app.apps.common.models import TimeStampedModel


class Car(TimeStampedModel):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        RESERVED = "reserved", "Reserved"
        RENTED = "rented", "Rented"
        SERVICE = "service", "In service"

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    vin = models.CharField(max_length=32, unique=True)
    type = models.CharField(max_length=50)
    base_price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    mileage = models.PositiveIntegerField(default=0)
    last_service_at = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.make} {self.model} ({self.year})"

    class Meta:
        ordering = ["make", "model", "year"]

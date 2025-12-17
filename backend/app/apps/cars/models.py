from uuid import uuid4

from django.db import models


class Car(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        RESERVED = "reserved", "Reserved"
        RENTED = "rented", "Rented"
        SERVICE = "service", "In Service"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    make = models.CharField(max_length=128)
    model = models.CharField(max_length=128)
    year = models.PositiveIntegerField()
    vin = models.CharField(max_length=17, unique=True)
    type = models.CharField(max_length=64)
    base_price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.AVAILABLE)
    mileage = models.PositiveIntegerField(default=0)
    last_service_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["make", "model", "year"]

    def __str__(self) -> str:  # pragma: no cover - presentation only
        return f"{self.make} {self.model} ({self.year})"

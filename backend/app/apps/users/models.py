from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        MANAGER = "manager", "Manager"
        ADMIN = "admin", "Admin"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    def __str__(self) -> str:  # pragma: no cover - delegated to AbstractUser
        return f"{self.username} ({self.get_role_display()})"


class CustomerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32)
    driver_license_no = models.CharField(max_length=64)
    address = models.TextField()

    def __str__(self) -> str:  # pragma: no cover - simple identity helper
        return self.full_name

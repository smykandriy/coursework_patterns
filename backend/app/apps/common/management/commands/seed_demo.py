from __future__ import annotations

from datetime import date, timedelta

from django.core.management.base import BaseCommand

from app.apps.bookings.services import BookingService
from app.apps.cars.models import Car
from app.apps.pricing.models import PricingRule
from app.apps.users.models import Customer, User


class Command(BaseCommand):
    help = "Seed demo data with users, cars, pricing rules, and a sample booking"

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "full_name": "Admin User",
                "role": User.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin.set_password("admin123")
        admin.save()

        manager, _ = User.objects.get_or_create(
            email="manager@example.com",
            defaults={"full_name": "Manager", "role": User.Role.MANAGER, "is_staff": True},
        )
        manager.set_password("manager123")
        manager.save()

        customer, _ = User.objects.get_or_create(
            email="customer@example.com",
            defaults={"full_name": "Customer", "role": User.Role.CUSTOMER},
        )
        customer.set_password("customer123")
        customer.save()
        Customer.objects.get_or_create(
            user=customer,
            defaults={"phone": "123456", "driver_license_no": "DL-1234", "address": "Main Street"},
        )

        car, _ = Car.objects.get_or_create(
            vin="VIN-DEMO-1",
            defaults={
                "make": "Toyota",
                "model": "Corolla",
                "year": 2022,
                "type": "sedan",
                "base_price_per_day": 70,
                "status": Car.Status.AVAILABLE,
                "mileage": 10000,
            },
        )

        PricingRule.objects.get_or_create(
            name="Weekly discount",
            strategy_type=PricingRule.StrategyType.DURATION,
            defaults={"params": {"thresholds": [{"days": 7, "discount_pct": 10}]}}
        )
        PricingRule.objects.get_or_create(
            name="Depreciation",
            strategy_type=PricingRule.StrategyType.YEAR,
            defaults={"params": {"per_year_pct": 2, "max_pct": 20}},
        )
        PricingRule.objects.get_or_create(
            name="Summer",
            strategy_type=PricingRule.StrategyType.SEASONAL,
            defaults={"params": {"seasons": [{"start": "06-01", "end": "08-31", "surcharge_pct": 5}]}},
        )

        service = BookingService()
        start = date.today() + timedelta(days=3)
        end = start + timedelta(days=5)
        if not car.bookings.filter(start_date=start, end_date=end).exists():
            service.create_booking(customer.customer_profile, car, start, end)
        self.stdout.write(self.style.SUCCESS("Seed data created."))

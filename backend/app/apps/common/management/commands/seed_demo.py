from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.bookings.models import Booking
from apps.bookings.services import BookingService
from apps.cars.models import Car
from apps.pricing.models import PricingRule
from apps.users.models import CustomerProfile


User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo data for development environments."

    def handle(self, *args, **options):
        with transaction.atomic():
            admin = self._get_or_create_user(
                username="admin",
                email="admin@example.com",
                password="adminpass",
                role=User.Role.ADMIN,
            )
            manager = self._get_or_create_user(
                username="manager",
                email="manager@example.com",
                password="managerpass",
                role=User.Role.MANAGER,
            )
            customer = self._get_or_create_user(
                username="customer",
                email="customer@example.com",
                password="customerpass",
                role=User.Role.CUSTOMER,
            )
            CustomerProfile.objects.get_or_create(
                user=customer,
                defaults={
                    "full_name": "Demo Customer",
                    "phone": "555-1000",
                    "driver_license_no": "DL-12345",
                    "address": "123 Demo Street",
                },
            )

            self.stdout.write(self.style.SUCCESS("Users ready: admin, manager, customer."))
            self._seed_cars()
            self._seed_pricing_rules()
            self._seed_bookings(customer)
            self.stdout.write(self.style.SUCCESS("Demo data seeded."))

    def _get_or_create_user(self, username: str, email: str, password: str, role: str) -> User:
        user, created = User.objects.get_or_create(
            username=username, defaults={"email": email, "role": role}
        )
        if created or not user.check_password(password):
            user.set_password(password)
            user.role = role
            user.email = email
            user.save()
        return user

    def _seed_cars(self) -> None:
        car_data = [
            ("Toyota", "Camry", 2022, "VIN00000000000001", "sedan", "85.00"),
            ("Honda", "Civic", 2021, "VIN00000000000002", "sedan", "78.00"),
            ("Ford", "Escape", 2020, "VIN00000000000003", "suv", "95.00"),
            ("Tesla", "Model 3", 2023, "VIN00000000000004", "sedan", "140.00"),
            ("Chevrolet", "Tahoe", 2019, "VIN00000000000005", "suv", "120.00"),
            ("BMW", "X5", 2022, "VIN00000000000006", "suv", "160.00"),
            ("Audi", "A4", 2021, "VIN00000000000007", "sedan", "130.00"),
            ("Hyundai", "Elantra", 2020, "VIN00000000000008", "sedan", "70.00"),
            ("Kia", "Sorento", 2022, "VIN00000000000009", "suv", "98.00"),
            ("Jeep", "Wrangler", 2021, "VIN00000000000010", "suv", "150.00"),
        ]
        for make, model, year, vin, car_type, base_price in car_data:
            Car.objects.get_or_create(
                vin=vin,
                defaults={
                    "make": make,
                    "model": model,
                    "year": year,
                    "type": car_type,
                    "base_price_per_day": Decimal(base_price),
                },
            )
        self.stdout.write(self.style.SUCCESS("Cars ready."))

    def _seed_pricing_rules(self) -> None:
        PricingRule.objects.get_or_create(
            name="Summer uplift",
            strategy_type=PricingRule.StrategyType.SEASONAL,
            params={"months": [6, 7, 8], "multiplier": 1.15},
            defaults={"active": True},
        )
        PricingRule.objects.get_or_create(
            name="Weekly discount",
            strategy_type=PricingRule.StrategyType.DURATION_DISCOUNT,
            params={"min_days": 7, "discount_rate": 0.1},
            defaults={"active": True},
        )
        PricingRule.objects.get_or_create(
            name="Annual depreciation",
            strategy_type=PricingRule.StrategyType.YEAR_DEPRECIATION,
            params={"rate": 0.03},
            defaults={"active": True},
        )
        self.stdout.write(self.style.SUCCESS("Pricing rules ready."))

    def _seed_bookings(self, customer: User) -> None:
        service = BookingService()
        cars = list(Car.objects.all()[:2])
        if not cars:
            return
        start = date.today() + timedelta(days=1)
        end = start + timedelta(days=3)
        existing = Booking.objects.filter(customer=customer).first()
        if existing:
            return
        booking = service.create_booking(
            customer=customer, car=cars[0], start_date=start, end_date=end
        )
        service.confirm_booking(booking)
        service.checkin_booking(booking)
        self.stdout.write(self.style.SUCCESS("Sample booking created."))

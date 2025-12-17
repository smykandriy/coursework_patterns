import os
from datetime import date, timedelta
from decimal import Decimal

import pytest


os.environ.setdefault("USE_SQLITE_FOR_TESTS", "1")


@pytest.fixture
def customer_user(django_user_model):
    return django_user_model.objects.create_user(username="customer", password="pass")


@pytest.fixture
def car():
    from apps.cars.models import Car

    return Car.objects.create(
        make="Test",
        model="Car",
        year=date.today().year,
        vin="VIN1234567890123",
        type="sedan",
        base_price_per_day=Decimal("100.00"),
    )


@pytest.fixture
def booking(customer_user, car):
    from apps.bookings.models import Booking

    return Booking.objects.create(
        customer=customer_user,
        car=car,
        start_date=date.today(),
        end_date=date.today() + timedelta(days=1),
    )

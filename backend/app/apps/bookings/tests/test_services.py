from datetime import date
from decimal import Decimal

import pytest

from app.apps.bookings.models import Booking, Deposit, Fine
from app.apps.bookings.services import BookingService
from app.apps.cars.models import Car
from app.apps.users.models import Customer, User


@pytest.mark.django_db
def test_booking_state_transitions_and_invoice():
    customer_user = User.objects.create_user(
        email="customer@example.com",
        password="pass",
        full_name="Customer",
        role=User.Role.CUSTOMER,
    )
    Customer.objects.create(
        user=customer_user,
        phone="123",
        driver_license_no="DL123",
        address="Main St",
    )
    car = Car.objects.create(
        make="Ford",
        model="Focus",
        year=2019,
        vin="VIN456",
        type="hatchback",
        base_price_per_day=80,
        status=Car.Status.AVAILABLE,
        mileage=5000,
    )

    service = BookingService()
    booking, suggested = service.create_booking(
        customer=customer_user.customer_profile,
        car=car,
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 5),
    )

    assert booking.status == Booking.Status.PENDING
    assert suggested > 0

    service.transition(booking).confirm()
    booking.refresh_from_db()
    assert booking.status == Booking.Status.CONFIRMED
    assert booking.deposit.status == Deposit.Status.HELD

    service.transition(booking).check_in()
    booking.refresh_from_db()
    assert booking.status == Booking.Status.ACTIVE

    service.transition(booking).complete(
        mileage_delta=100,
        fines=[{"type": Fine.Type.LATE_RETURN, "amount": Decimal("25.00"), "notes": "Late"}],
    )
    booking.refresh_from_db()
    assert booking.status == Booking.Status.COMPLETED
    assert booking.invoice.amount_total >= booking.invoice.amount_rental
    assert booking.fines.count() == 1
    assert booking.deposit.status in {Deposit.Status.RELEASED, Deposit.Status.FORFEITED}

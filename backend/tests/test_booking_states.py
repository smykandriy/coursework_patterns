from decimal import Decimal

import pytest

from apps.bookings.models import Booking, Fine
from apps.bookings.services import BookingOverlapError, BookingService, InvalidStateTransition
from apps.common.event_bus import BOOKING_CONFIRMED, CAR_RETURNED, event_bus


@pytest.mark.django_db
def test_state_transitions_update_car_and_emit_events(booking):
    service = BookingService()
    events: list[str] = []
    event_bus.clear()
    event_bus.subscribe(BOOKING_CONFIRMED, lambda payload: events.append(payload.status))
    event_bus.subscribe(CAR_RETURNED, lambda payload: events.append(payload.status))

    service.confirm_booking(booking)
    booking.refresh_from_db()
    booking.car.refresh_from_db()
    assert booking.status == Booking.Status.CONFIRMED
    assert booking.car.status == booking.car.Status.RESERVED

    service.checkin_booking(booking)
    booking.refresh_from_db()
    booking.car.refresh_from_db()
    assert booking.status == Booking.Status.ACTIVE
    assert booking.car.status == booking.car.Status.RENTED

    service.return_booking(booking)
    booking.refresh_from_db()
    booking.car.refresh_from_db()
    assert booking.status == Booking.Status.COMPLETED
    assert booking.car.status == booking.car.Status.AVAILABLE

    assert Booking.Status.CONFIRMED in events
    assert Booking.Status.COMPLETED in events


@pytest.mark.django_db
def test_invalid_transition_raises(booking):
    service = BookingService()
    with pytest.raises(InvalidStateTransition):
        service.return_booking(booking)


@pytest.mark.django_db
def test_overlap_detection(booking, customer_user, car):
    service = BookingService()
    assert service.has_overlaps(car, booking.start_date, booking.end_date)

    gap = booking.end_date - booking.start_date
    assert not service.has_overlaps(
        car,
        booking.end_date + gap,
        booking.end_date + gap * 2,
    )

    with pytest.raises(BookingOverlapError):
        service.create_booking(customer_user, car, booking.start_date, booking.end_date)


@pytest.mark.django_db
def test_invoice_builder_totals_with_fines(booking):
    service = BookingService()
    service.apply_fine(booking, Fine.FineType.DAMAGE, Decimal("50.00"), notes="Scratch")
    result = service.build_invoice(booking)

    invoice = result["invoice"]
    assert invoice.total == Decimal("150.00")
    assert len(invoice.breakdown) == 2
    assert any(item["label"].startswith("Fine") for item in invoice.breakdown)

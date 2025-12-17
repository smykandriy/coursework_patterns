from datetime import date
from decimal import Decimal

from django.db import transaction

from apps.common.event_bus import FINE_APPLIED, event_bus
from apps.pricing.services import PricingService

from .invoice_builder import InvoiceBuilder
from .models import Booking, Fine
from .state import BookingStateMachine, InvalidStateTransition


class BookingOverlapError(Exception):
    pass


class BookingService:
    def __init__(self, pricing_service: PricingService | None = None, state_machine=None) -> None:
        self.pricing_service = pricing_service or PricingService()
        self.state_machine = state_machine or BookingStateMachine()

    def has_overlaps(self, car, start_date: date, end_date: date, exclude_booking_id=None) -> bool:
        qs = Booking.objects.filter(
            car=car,
            status__in=[Booking.Status.PENDING, Booking.Status.CONFIRMED, Booking.Status.ACTIVE],
            start_date__lt=end_date,
            end_date__gt=start_date,
        )
        if exclude_booking_id:
            qs = qs.exclude(id=exclude_booking_id)
        return qs.exists()

    @transaction.atomic
    def create_booking(self, customer, car, start_date: date, end_date: date) -> Booking:
        if end_date <= start_date:
            raise ValueError("End date must be after start date")
        if self.has_overlaps(car, start_date, end_date):
            raise BookingOverlapError("Car already booked for the selected period")
        return Booking.objects.create(customer=customer, car=car, start_date=start_date, end_date=end_date)

    def confirm_booking(self, booking: Booking) -> Booking:
        return self.state_machine.transition(booking, Booking.Status.CONFIRMED)

    def checkin_booking(self, booking: Booking) -> Booking:
        return self.state_machine.transition(booking, Booking.Status.ACTIVE)

    def return_booking(self, booking: Booking) -> Booking:
        return self.state_machine.transition(booking, Booking.Status.COMPLETED)

    def cancel_booking(self, booking: Booking) -> Booking:
        return self.state_machine.transition(booking, Booking.Status.CANCELED)

    def apply_fine(self, booking: Booking, fine_type: str, amount: Decimal, notes: str = "") -> Fine:
        fine = Fine.objects.create(booking=booking, type=fine_type, amount=amount, notes=notes)
        event_bus.publish(FINE_APPLIED, fine)
        return fine

    def build_invoice(self, booking: Booking) -> dict:
        quote = self.pricing_service.quote(booking.car, booking.start_date, booking.end_date)
        builder = InvoiceBuilder(booking)
        builder.add_pricing_breakdown(quote["breakdown"])
        builder.add_fines(list(booking.fines.all()))
        invoice = builder.build()
        return {"invoice": invoice, "pricing": quote}


__all__ = [
    "BookingService",
    "BookingOverlapError",
    "InvalidStateTransition",
]

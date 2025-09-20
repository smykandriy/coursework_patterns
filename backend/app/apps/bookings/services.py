from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Sequence

from django.db import transaction

from app.apps.bookings.models import Booking, Deposit, Fine, Invoice
from app.apps.cars.models import Car
from app.apps.common.models import BookingEvent, event_bus
from app.apps.payments.services import PaymentProviderFactory
from app.apps.pricing.services import PricingService
from app.apps.users.models import Customer


class BookingError(Exception):
    pass


class BookingState:
    """State pattern for booking lifecycle."""

    name = "base"

    def __init__(self, booking: Booking, service: "BookingService") -> None:
        self.booking = booking
        self.service = service

    def confirm(self) -> Booking:
        raise BookingError("Cannot confirm from current state")

    def check_in(self) -> Booking:
        raise BookingError("Cannot check-in from current state")

    def complete(self, mileage_delta: int, fines: Sequence[dict[str, str | float]]) -> Booking:
        raise BookingError("Cannot complete from current state")

    def cancel(self) -> Booking:
        raise BookingError("Cannot cancel from current state")


class PendingState(BookingState):
    name = Booking.Status.PENDING

    def confirm(self) -> Booking:
        return self.service._confirm_booking(self.booking)

    def cancel(self) -> Booking:
        self.booking.status = Booking.Status.CANCELED
        self.booking.save(update_fields=["status"])
        return self.booking


class ConfirmedState(BookingState):
    name = Booking.Status.CONFIRMED

    def check_in(self) -> Booking:
        return self.service._activate_booking(self.booking)

    def cancel(self) -> Booking:
        self.booking.status = Booking.Status.CANCELED
        self.booking.save(update_fields=["status"])
        if self.booking.deposit:
            provider = PaymentProviderFactory.get_provider()
            provider.release_deposit(self.booking.deposit)
            self.booking.deposit.status = Deposit.Status.RELEASED
            self.booking.deposit.save(update_fields=["status"])
        self.booking.car.status = Car.Status.AVAILABLE
        self.booking.car.save(update_fields=["status"])
        return self.booking


class ActiveState(BookingState):
    name = Booking.Status.ACTIVE

    def complete(self, mileage_delta: int, fines: Sequence[dict[str, str | float]]) -> Booking:
        return self.service._complete_booking(self.booking, mileage_delta, fines)


class BookingStateFactory:
    @staticmethod
    def get_state(booking: Booking, service: "BookingService") -> BookingState:
        mapping = {
            Booking.Status.PENDING: PendingState,
            Booking.Status.CONFIRMED: ConfirmedState,
            Booking.Status.ACTIVE: ActiveState,
        }
        state_cls = mapping.get(booking.status, BookingState)
        return state_cls(booking, service)


@dataclass
class InvoiceBuilder:
    """Builder pattern assembling invoice details."""

    rental_amount: Decimal = Decimal("0")
    fee_amount: Decimal = Decimal("0")
    fine_amount: Decimal = Decimal("0")

    def reset(self) -> None:
        self.rental_amount = Decimal("0")
        self.fee_amount = Decimal("0")
        self.fine_amount = Decimal("0")

    def with_rental(self, amount: Decimal) -> "InvoiceBuilder":
        self.rental_amount = amount
        return self

    def with_fees(self, amount: Decimal) -> "InvoiceBuilder":
        self.fee_amount = amount
        return self

    def with_fines(self, amount: Decimal) -> "InvoiceBuilder":
        self.fine_amount = amount
        return self

    def build(self, booking: Booking) -> Invoice:
        total = self.rental_amount + self.fee_amount + self.fine_amount
        invoice, _ = Invoice.objects.update_or_create(
            booking=booking,
            defaults={
                "amount_rental": self.rental_amount,
                "amount_fees": self.fee_amount,
                "amount_fines": self.fine_amount,
                "amount_total": total,
            },
        )
        return invoice


@dataclass
class BookingService:
    pricing_service: PricingService = field(default_factory=PricingService)

    def _get_state(self, booking: Booking) -> BookingState:
        return BookingStateFactory.get_state(booking, self)

    def create_booking(
        self,
        customer: Customer,
        car: Car,
        start_date: date,
        end_date: date,
        notes: str = "",
    ) -> tuple[Booking, Decimal]:
        if Booking.objects.active().filter(car=car, start_date__lt=end_date, end_date__gt=start_date).exists():
            raise BookingError("Car already booked for selected dates")
        booking = Booking.objects.create(
            customer=customer,
            car=car,
            start_date=start_date,
            end_date=end_date,
            notes=notes,
        )
        quote = self.pricing_service.quote(car, start_date, end_date)
        deposit_amount = Decimal(str(quote["total"])) * Decimal("0.3")
        return booking, deposit_amount.quantize(Decimal("0.01"))

    @transaction.atomic
    def _confirm_booking(self, booking: Booking) -> Booking:
        if booking.status != Booking.Status.PENDING:
            raise BookingError("Only pending bookings can be confirmed")
        booking.status = Booking.Status.CONFIRMED
        booking.save(update_fields=["status"])
        booking.car.status = Car.Status.RESERVED
        booking.car.save(update_fields=["status"])
        quote = self.pricing_service.quote(booking.car, booking.start_date, booking.end_date)
        deposit_amount = Decimal(str(quote["total"])) * Decimal("0.3")
        deposit, _ = Deposit.objects.update_or_create(
            booking=booking,
            defaults={"amount": deposit_amount.quantize(Decimal("0.01"))},
        )
        provider = PaymentProviderFactory.get_provider()
        deposit.txn_ref = provider.hold_deposit(deposit)
        deposit.status = Deposit.Status.HELD
        deposit.save(update_fields=["txn_ref", "status", "amount"])
        event_bus.publish(BookingEvent(name="booking.confirmed", payload={"booking_id": str(booking.id)}))
        return booking

    @transaction.atomic
    def _activate_booking(self, booking: Booking) -> Booking:
        if booking.status != Booking.Status.CONFIRMED:
            raise BookingError("Booking must be confirmed first")
        booking.status = Booking.Status.ACTIVE
        booking.save(update_fields=["status"])
        booking.car.status = Car.Status.RENTED
        booking.car.save(update_fields=["status"])
        return booking

    @transaction.atomic
    def _complete_booking(
        self,
        booking: Booking,
        mileage_delta: int,
        fines: Sequence[dict[str, str | float]],
    ) -> Booking:
        if booking.status != Booking.Status.ACTIVE:
            raise BookingError("Only active bookings can be completed")
        booking.status = Booking.Status.COMPLETED
        booking.save(update_fields=["status"])
        car = booking.car
        car.status = Car.Status.AVAILABLE
        car.mileage += mileage_delta
        car.save(update_fields=["status", "mileage"])

        fines_total = Decimal("0")
        for fine_data in fines:
            amount = Decimal(str(fine_data.get("amount", 0)))
            Fine.objects.create(
                booking=booking,
                type=fine_data.get("type", Fine.Type.OTHER),
                amount=amount,
                notes=fine_data.get("notes", ""),
            )
            fines_total += amount
            event_bus.publish(
                BookingEvent(
                    name="fine.applied",
                    payload={"booking_id": str(booking.id), "amount": float(amount)},
                )
            )

        quote = self.pricing_service.quote(car, booking.start_date, booking.end_date)
        rental_amount = Decimal(str(quote["total"])).quantize(Decimal("0.01"))
        builder = InvoiceBuilder().with_rental(rental_amount).with_fees(Decimal("0")).with_fines(fines_total)
        invoice = builder.build(booking)

        provider = PaymentProviderFactory.get_provider()
        if booking.deposit:
            if fines_total > Decimal("0") and fines_total > booking.deposit.amount:
                booking.deposit.status = Deposit.Status.FORFEITED
                booking.deposit.txn_ref = provider.forfeit_deposit(booking.deposit)
            else:
                booking.deposit.status = Deposit.Status.RELEASED
                booking.deposit.txn_ref = provider.release_deposit(booking.deposit)
            booking.deposit.save(update_fields=["status", "txn_ref"])

        provider.pay_invoice(invoice)
        event_bus.publish(BookingEvent(name="booking.completed", payload={"booking_id": str(booking.id)}))
        return booking

    def transition(self, booking: Booking) -> BookingState:
        return self._get_state(booking)

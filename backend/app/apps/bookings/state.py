from dataclasses import dataclass

from apps.cars.models import Car
from apps.common.event_bus import CAR_RETURNED, BOOKING_CONFIRMED, event_bus

from .models import Booking


class InvalidStateTransition(Exception):
    pass


CAR_STATUS_BY_BOOKING: dict[str, str] = {
    Booking.Status.CONFIRMED: Car.Status.RESERVED,
    Booking.Status.ACTIVE: Car.Status.RENTED,
    Booking.Status.COMPLETED: Car.Status.AVAILABLE,
    Booking.Status.CANCELED: Car.Status.AVAILABLE,
}


@dataclass
class BookingState:
    booking: Booking

    def transition_to(self, target_status: str) -> Booking:
        if target_status not in self.allowed_transitions:
            raise InvalidStateTransition(
                f"Cannot transition booking from {self.booking.status} to {target_status}"
            )

        self.booking.status = target_status
        car_status = CAR_STATUS_BY_BOOKING.get(target_status)
        if car_status:
            self.booking.car.status = car_status
            self.booking.car.save(update_fields=["status"])
        self.booking.save(update_fields=["status", "updated_at"])
        self._emit_events(target_status)
        return self.booking

    @property
    def allowed_transitions(self) -> tuple[str, ...]:
        return ()

    def _emit_events(self, target_status: str) -> None:
        if target_status == Booking.Status.CONFIRMED:
            event_bus.publish(BOOKING_CONFIRMED, self.booking)
        if target_status == Booking.Status.COMPLETED:
            event_bus.publish(CAR_RETURNED, self.booking)


class PendingState(BookingState):
    @property
    def allowed_transitions(self) -> tuple[str, ...]:
        return (Booking.Status.CONFIRMED, Booking.Status.CANCELED)


class ConfirmedState(BookingState):
    @property
    def allowed_transitions(self) -> tuple[str, ...]:
        return (Booking.Status.ACTIVE, Booking.Status.CANCELED)


class ActiveState(BookingState):
    @property
    def allowed_transitions(self) -> tuple[str, ...]:
        return (Booking.Status.COMPLETED, Booking.Status.CANCELED)


class CompletedState(BookingState):
    @property
    def allowed_transitions(self) -> tuple[str, ...]:
        return ()


class CanceledState(BookingState):
    @property
    def allowed_transitions(self) -> tuple[str, ...]:
        return ()


STATE_FACTORY = {
    Booking.Status.PENDING: PendingState,
    Booking.Status.CONFIRMED: ConfirmedState,
    Booking.Status.ACTIVE: ActiveState,
    Booking.Status.COMPLETED: CompletedState,
    Booking.Status.CANCELED: CanceledState,
}


class BookingStateMachine:
    def transition(self, booking: Booking, target_status: str) -> Booking:
        state_cls = STATE_FACTORY.get(booking.status)
        if not state_cls:
            raise InvalidStateTransition(f"No state registered for {booking.status}")
        state = state_cls(booking)
        return state.transition_to(target_status)

from collections import defaultdict
from typing import Any, Callable, Dict, Iterable, List


Handler = Callable[[Any], None]


class EventBus:
    def __init__(self) -> None:
        self._handlers: Dict[str, List[Handler]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: Handler) -> None:
        self._handlers[event_name].append(handler)

    def publish(self, event_name: str, payload: Any) -> None:
        for handler in list(self._handlers.get(event_name, [])):
            handler(payload)

    def subscriptions(self, event_name: str) -> Iterable[Handler]:
        return tuple(self._handlers.get(event_name, []))

    def clear(self) -> None:
        self._handlers.clear()


event_bus = EventBus()

BOOKING_CONFIRMED = "BookingConfirmed"
CAR_RETURNED = "CarReturned"
FINE_APPLIED = "FineApplied"

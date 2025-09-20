from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any, Callable, DefaultDict, Dict, Iterable, List, Protocol

from collections import defaultdict
from django.db import models


class TimeStampedModel(models.Model):
    """Base model with UUID primary key and created/updated timestamps."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DomainEvent(Protocol):
    """Marker protocol for events."""

    name: str


EventHandler = Callable[[DomainEvent], None]


class EventBus:
    """Simple in-memory event bus implementing the Observer pattern."""

    def __init__(self) -> None:
        self._subscribers: DefaultDict[str, List[EventHandler]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        self._subscribers[event_name].append(handler)

    def publish(self, event: DomainEvent) -> None:
        for handler in self._subscribers.get(event.name, []):
            handler(event)


event_bus = EventBus()


@dataclass(slots=True)
class BookingEvent:
    name: str
    payload: Dict[str, Any]


def log_event(event: DomainEvent) -> None:
    """Console logger handler used in tests/demo."""

    print(f"[event] {event.name}: {event}")


event_bus.subscribe("booking.confirmed", log_event)
event_bus.subscribe("booking.completed", log_event)
event_bus.subscribe("fine.applied", log_event)

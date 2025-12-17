from decimal import Decimal
from typing import Iterable

from .models import Invoice


class InvoiceBuilder:
    def __init__(self, booking) -> None:
        self.booking = booking
        self._items: list[dict] = []

    def add_charge(self, label: str, amount: Decimal, metadata: dict | None = None) -> None:
        self._items.append(
            {
                "label": label,
                "amount": str(Decimal(amount)),
                "metadata": metadata or {},
            }
        )

    def add_pricing_breakdown(self, breakdown: Iterable[dict]) -> None:
        for item in breakdown:
            self.add_charge(
                item.get("name", "Charge"), item.get("amount", 0), item.get("metadata", {})
            )

    def add_fines(self, fines: Iterable) -> None:
        for fine in fines:
            self.add_charge(
                f"Fine: {fine.get_type_display()}",
                fine.amount,
                {"type": fine.type, "fine_id": str(fine.id)},
            )

    def build(self) -> Invoice:
        total = sum(Decimal(item["amount"]) for item in self._items)
        invoice, _ = Invoice.objects.update_or_create(
            booking=self.booking,
            defaults={"breakdown": self._items, "total": total},
        )
        return invoice

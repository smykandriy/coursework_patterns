from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from app.apps.bookings.models import Deposit, Invoice


class PaymentProvider(Protocol):
    def hold_deposit(self, deposit: Deposit) -> str: ...

    def release_deposit(self, deposit: Deposit) -> str: ...

    def forfeit_deposit(self, deposit: Deposit) -> str: ...

    def pay_invoice(self, invoice: Invoice) -> str: ...


@dataclass(slots=True)
class MockPaymentProvider:
    name: str = "MockPay"

    def _reference(self, prefix: str) -> str:
        return f"{prefix}-{self.name.lower()}"

    def hold_deposit(self, deposit: Deposit) -> str:
        return self._reference("hold")

    def release_deposit(self, deposit: Deposit) -> str:
        return self._reference("release")

    def forfeit_deposit(self, deposit: Deposit) -> str:
        return self._reference("forfeit")

    def pay_invoice(self, invoice: Invoice) -> str:
        return self._reference("invoice")


class PaymentProviderFactory:
    """Abstract Factory returning payment providers."""

    @staticmethod
    def get_provider(provider: str | None = None) -> PaymentProvider:
        # In a real system this could switch between Stripe, PayPal, etc.
        return MockPaymentProvider(name=provider or "MockPay")

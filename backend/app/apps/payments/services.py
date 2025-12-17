from decimal import Decimal

from django.utils import timezone

from apps.bookings.models import Deposit, Invoice

from .factory import PaymentProviderFactory


class PaymentService:
    def __init__(self, provider_factory: PaymentProviderFactory | None = None) -> None:
        self.provider_factory = provider_factory or PaymentProviderFactory()

    def hold_deposit(self, booking, amount: Decimal) -> Deposit:
        provider = self.provider_factory.get_deposit_provider()
        txn_ref = provider.hold(amount)
        deposit, _ = Deposit.objects.update_or_create(
            booking=booking,
            defaults={"amount": amount, "status": Deposit.Status.HELD, "txn_ref": txn_ref},
        )
        return deposit

    def release_deposit(self, deposit: Deposit, partial: bool = False) -> Deposit:
        provider = self.provider_factory.get_deposit_provider()
        txn_ref = provider.release(deposit.amount)
        deposit.status = Deposit.Status.PARTIALLY_RELEASED if partial else Deposit.Status.RELEASED
        deposit.txn_ref = txn_ref
        deposit.save(update_fields=["status", "txn_ref", "updated_at"])
        return deposit

    def forfeit_deposit(self, deposit: Deposit) -> Deposit:
        provider = self.provider_factory.get_deposit_provider()
        txn_ref = provider.forfeit(deposit.amount)
        deposit.status = Deposit.Status.FORFEITED
        deposit.txn_ref = txn_ref
        deposit.save(update_fields=["status", "txn_ref", "updated_at"])
        return deposit

    def pay_invoice(self, invoice: Invoice, method: str) -> Invoice:
        provider = self.provider_factory.get_invoice_provider()
        txn_ref = provider.pay(invoice.total, method)
        invoice.method = method
        invoice.paid_at = timezone.now()
        invoice.payment_reference = txn_ref
        invoice.save(update_fields=["method", "paid_at", "payment_reference", "updated_at"])
        return invoice

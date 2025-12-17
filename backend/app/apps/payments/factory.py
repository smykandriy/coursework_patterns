from uuid import uuid4


class MockDepositProvider:
    def hold(self, amount):
        return f"hold-{uuid4()}-{amount}"

    def release(self, amount):
        return f"release-{uuid4()}-{amount}"

    def forfeit(self, amount):
        return f"forfeit-{uuid4()}-{amount}"


class MockInvoiceProvider:
    def pay(self, amount, method):
        return f"payment-{uuid4()}-{method}-{amount}"


class PaymentProviderFactory:
    def get_deposit_provider(self):
        return MockDepositProvider()

    def get_invoice_provider(self):
        return MockInvoiceProvider()

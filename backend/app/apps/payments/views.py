from __future__ import annotations

from django.shortcuts import get_object_or_404
from rest_framework import permissions, response, status
from rest_framework.views import APIView

from app.apps.bookings.models import Deposit, Invoice
from app.apps.bookings.serializers import DepositSerializer, InvoiceSerializer
from app.apps.payments.services import PaymentProviderFactory


class DepositActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_id, action: str):
        if request.user.role not in {"manager", "admin"}:
            return response.Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        deposit = get_object_or_404(Deposit, booking__id=booking_id)
        provider = PaymentProviderFactory.get_provider()
        if action == "hold":
            deposit.txn_ref = provider.hold_deposit(deposit)
            deposit.status = Deposit.Status.HELD
        elif action == "release":
            deposit.txn_ref = provider.release_deposit(deposit)
            deposit.status = Deposit.Status.RELEASED
        elif action == "forfeit":
            deposit.txn_ref = provider.forfeit_deposit(deposit)
            deposit.status = Deposit.Status.FORFEITED
        else:
            return response.Response({"detail": "Unknown action"}, status=status.HTTP_400_BAD_REQUEST)
        deposit.save(update_fields=["txn_ref", "status"])
        return response.Response(DepositSerializer(deposit).data)


class InvoicePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, booking_id):
        invoice = get_object_or_404(Invoice, booking__id=booking_id)
        if request.user.role not in {"manager", "admin"} and invoice.booking.customer.user != request.user:
            return response.Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        provider = PaymentProviderFactory.get_provider()
        invoice.method = request.data.get("method", "card")
        invoice.mark_paid(invoice.method)
        provider.pay_invoice(invoice)
        return response.Response(InvoiceSerializer(invoice).data)

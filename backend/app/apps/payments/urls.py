from __future__ import annotations

from django.urls import path

from app.apps.payments.views import DepositActionView, InvoicePaymentView

urlpatterns = [
    path("deposits/<uuid:booking_id>/<str:action>/", DepositActionView.as_view(), name="deposit-action"),
    path("invoices/<uuid:booking_id>/pay/", InvoicePaymentView.as_view(), name="invoice-pay"),
]

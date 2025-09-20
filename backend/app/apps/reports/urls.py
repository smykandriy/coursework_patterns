from __future__ import annotations

from django.urls import path

from app.apps.reports.views import CarReportView, FinancialReportView, FleetUtilizationView

urlpatterns = [
    path("reports/fleet-utilization/", FleetUtilizationView.as_view(), name="report-fleet"),
    path("reports/financials/", FinancialReportView.as_view(), name="report-financial"),
    path("reports/car/<uuid:car_id>/", CarReportView.as_view(), name="report-car"),
]

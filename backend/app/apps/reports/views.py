from __future__ import annotations

from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import permissions, response, status
from rest_framework.views import APIView

from app.apps.cars.models import Car
from app.apps.reports.services import ReportService


class ReportsBaseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_period(self, request):
        date_from = request.query_params.get("from")
        date_to = request.query_params.get("to")
        if not date_from or not date_to:
            return None, None
        return datetime.fromisoformat(date_from).date(), datetime.fromisoformat(date_to).date()


class FleetUtilizationView(ReportsBaseView):
    def get(self, request, *args, **kwargs):
        start, end = self.get_period(request)
        if not start or not end:
            return response.Response({"detail": "Provide from/to"}, status=status.HTTP_400_BAD_REQUEST)
        report = ReportService.fleet_utilization(start, end)
        return response.Response(report.__dict__)


class FinancialReportView(ReportsBaseView):
    def get(self, request, *args, **kwargs):
        start, end = self.get_period(request)
        if not start or not end:
            return response.Response({"detail": "Provide from/to"}, status=status.HTTP_400_BAD_REQUEST)
        report = ReportService.financials(start, end)
        return response.Response(report.__dict__)


class CarReportView(ReportsBaseView):
    def get(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        if request.user.role not in {"admin", "manager"}:
            return response.Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        report = ReportService.car_report(car)
        return response.Response(report)

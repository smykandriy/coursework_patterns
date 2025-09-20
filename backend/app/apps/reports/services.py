from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Dict

from django.db.models import Sum

from app.apps.bookings.models import Booking, Invoice
from app.apps.cars.models import Car


@dataclass
class FleetUtilizationReport:
    period_from: date
    period_to: date
    utilization_pct: float
    total_bookings: int


@dataclass
class FinancialReport:
    period_from: date
    period_to: date
    rental_revenue: float
    fines_total: float
    deposits_held: float


class ReportService:
    @staticmethod
    def fleet_utilization(period_from: date, period_to: date) -> FleetUtilizationReport:
        total_cars = Car.objects.count() or 1
        booking_days = Booking.objects.filter(
            start_date__lt=period_to,
            end_date__gt=period_from,
        ).count() * 1  # simplified: count bookings as single day blocks
        total_days = total_cars * max(1, (period_to - period_from).days)
        utilization = float(booking_days / total_days * 100)
        return FleetUtilizationReport(
            period_from=period_from,
            period_to=period_to,
            utilization_pct=round(utilization, 2),
            total_bookings=booking_days,
        )

    @staticmethod
    def financials(period_from: date, period_to: date) -> FinancialReport:
        invoices = Invoice.objects.filter(
            booking__start_date__gte=period_from,
            booking__end_date__lte=period_to,
        )
        rental = invoices.aggregate(total=Sum("amount_rental"))["total"] or Decimal("0")
        fines = invoices.aggregate(total=Sum("amount_fines"))["total"] or Decimal("0")
        deposits = (
            Booking.objects.filter(created_at__range=(period_from, period_to), deposit__isnull=False)
            .aggregate(total=Sum("deposit__amount"))["total"]
            or Decimal("0")
        )
        return FinancialReport(
            period_from=period_from,
            period_to=period_to,
            rental_revenue=float(rental),
            fines_total=float(fines),
            deposits_held=float(deposits),
        )

    @staticmethod
    def car_report(car: Car) -> Dict[str, float]:
        bookings = car.bookings.all()
        total_days = sum(b.duration_days() for b in bookings)
        revenue = (
            Invoice.objects.filter(booking__car=car).aggregate(total=Sum("amount_total"))["total"]
            or Decimal("0")
        )
        return {"total_days": total_days, "revenue": float(revenue)}

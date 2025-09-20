from __future__ import annotations

from django.shortcuts import get_object_or_404
from rest_framework import permissions, response, status, viewsets
from rest_framework.decorators import action

from app.apps.bookings.models import Booking
from app.apps.bookings.serializers import (
    BookingCreateSerializer,
    BookingReturnSerializer,
    BookingSerializer,
    FineSerializer,
)
from app.apps.bookings.services import BookingService
from app.apps.cars.models import Car


class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in {"manager", "admin"}


class BookingViewSet(viewsets.ModelViewSet):
    queryset = (
        Booking.objects.select_related("customer__user", "car")
        .prefetch_related("fines")
        .all()
    )
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    service_class = BookingService

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_superuser or user.role in {"admin", "manager"}:
            return qs
        return qs.filter(customer__user=user)

    def create(self, request, *args, **kwargs):
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.is_authenticated or user.role != "customer":
            return response.Response({"detail": "Only customers can create bookings."}, status=status.HTTP_403_FORBIDDEN)
        if not hasattr(user, "customer_profile"):
            return response.Response({"detail": "Customer profile missing."}, status=status.HTTP_400_BAD_REQUEST)
        car = get_object_or_404(Car, id=serializer.validated_data["car_id"])
        service = self.service_class()
        booking, deposit = service.create_booking(
            customer=user.customer_profile,
            car=car,
            start_date=serializer.validated_data["start_date"],
            end_date=serializer.validated_data["end_date"],
            notes=serializer.validated_data.get("notes", ""),
        )
        data = BookingSerializer(booking, context={"request": request}).data
        data["deposit_suggested"] = float(deposit)
        headers = self.get_success_headers(data)
        return response.Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["post"], permission_classes=[IsManagerOrAdmin])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        service = self.service_class()
        service.transition(booking).confirm()
        booking.refresh_from_db()
        return response.Response(BookingSerializer(booking).data)

    @action(detail=True, methods=["post"], permission_classes=[IsManagerOrAdmin])
    def checkin(self, request, pk=None):
        booking = self.get_object()
        service = self.service_class()
        service.transition(booking).check_in()
        booking.refresh_from_db()
        return response.Response(BookingSerializer(booking).data)

    @action(detail=True, methods=["post"], permission_classes=[IsManagerOrAdmin])
    def return_car(self, request, pk=None):
        booking = self.get_object()
        serializer = BookingReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = self.service_class()
        service.transition(booking).complete(
            mileage_delta=serializer.validated_data["mileage_delta"],
            fines=serializer.validated_data["fines"],
        )
        booking.refresh_from_db()
        return response.Response(BookingSerializer(booking).data)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        service = self.service_class()
        try:
            service.transition(booking).cancel()
        except Exception as exc:  # pragma: no cover - ensures message returned
            return response.Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        booking.refresh_from_db()
        return response.Response(BookingSerializer(booking).data)

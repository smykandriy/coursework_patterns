from decimal import Decimal, InvalidOperation

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.common.permissions import IsManagerOrAdmin
from apps.payments.services import PaymentService

from .models import Booking
from .serializers import BookingSerializer, FineSerializer
from .services import BookingOverlapError, BookingService, InvalidStateTransition


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post"]

    @property
    def booking_service(self) -> BookingService:
        if not hasattr(self, "_booking_service"):
            self._booking_service = BookingService()
        return self._booking_service

    @property
    def payment_service(self) -> PaymentService:
        if not hasattr(self, "_payment_service"):
            self._payment_service = PaymentService()
        return self._payment_service

    def get_queryset(self):
        base_qs = Booking.objects.select_related("customer", "car").prefetch_related("fines")
        user = self.request.user
        if user.role in (user.Role.ADMIN, user.Role.MANAGER):
            return base_qs
        return base_qs.filter(customer=user)

    def perform_create(self, serializer):
        try:
            booking = self.booking_service.create_booking(
                customer=self.request.user,
                car=serializer.validated_data["car"],
                start_date=serializer.validated_data["start_date"],
                end_date=serializer.validated_data["end_date"],
            )
        except (ValueError, BookingOverlapError) as exc:
            raise ValidationError(str(exc))
        serializer.instance = booking

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["post"], permission_classes=[IsManagerOrAdmin])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        try:
            booking = self.booking_service.confirm_booking(booking)
        except InvalidStateTransition as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(booking).data)

    @action(detail=True, methods=["post"], permission_classes=[IsManagerOrAdmin])
    def checkin(self, request, pk=None):
        booking = self.get_object()
        try:
            booking = self.booking_service.checkin_booking(booking)
        except InvalidStateTransition as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(booking).data)

    @action(detail=True, methods=["post"], url_path="return", permission_classes=[IsManagerOrAdmin])
    def return_booking(self, request, pk=None):
        booking = self.get_object()
        try:
            booking = self.booking_service.return_booking(booking)
        except InvalidStateTransition as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(booking).data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        user = request.user
        if user.role not in (user.Role.MANAGER, user.Role.ADMIN) and booking.customer != user:
            return Response(
                {"detail": "Not allowed to cancel this booking."}, status=status.HTTP_403_FORBIDDEN
            )
        try:
            booking = self.booking_service.cancel_booking(booking)
        except InvalidStateTransition as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(booking).data)

    @action(detail=True, methods=["get", "post"], url_path="fines")
    def fines(self, request, pk=None):
        booking = self.get_object()
        if request.method.lower() == "get":
            fines = booking.fines.all()
            return Response(FineSerializer(fines, many=True).data)

        if request.user.role not in (request.user.Role.ADMIN, request.user.Role.MANAGER):
            return Response(
                {"detail": "Only managers can add fines."}, status=status.HTTP_403_FORBIDDEN
            )
        serializer = FineSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fine_type = serializer.validated_data["type"]
        try:
            amount = Decimal(serializer.validated_data["amount"])
        except (InvalidOperation, TypeError):
            raise ValidationError("Invalid fine amount.")
        notes = serializer.validated_data.get("notes", "")
        fine = self.booking_service.apply_fine(booking, fine_type, amount, notes)
        return Response(FineSerializer(fine).data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["post"],
        url_path="deposit/hold",
        permission_classes=[IsManagerOrAdmin],
    )
    def hold_deposit(self, request, pk=None):
        booking = self.get_object()
        amount = request.data.get("amount")
        if amount is None:
            return Response({"detail": "amount is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decimal_amount = Decimal(amount)
        except (InvalidOperation, TypeError):
            raise ValidationError("Invalid deposit amount.")
        deposit = self.payment_service.hold_deposit(booking, decimal_amount)
        return Response(
            {"id": str(deposit.id), "status": deposit.status, "amount": str(deposit.amount)}
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="deposit/release",
        permission_classes=[IsManagerOrAdmin],
    )
    def release_deposit(self, request, pk=None):
        booking = self.get_object()
        if not hasattr(booking, "deposit"):
            return Response(
                {"detail": "No deposit to release."}, status=status.HTTP_400_BAD_REQUEST
            )
        partial_flag = str(request.data.get("partial", False)).lower() in ("true", "1", "yes")
        deposit = self.payment_service.release_deposit(booking.deposit, partial=partial_flag)
        return Response(
            {"id": str(deposit.id), "status": deposit.status, "amount": str(deposit.amount)}
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="deposit/forfeit",
        permission_classes=[IsManagerOrAdmin],
    )
    def forfeit_deposit(self, request, pk=None):
        booking = self.get_object()
        if not hasattr(booking, "deposit"):
            return Response(
                {"detail": "No deposit to forfeit."}, status=status.HTTP_400_BAD_REQUEST
            )
        deposit = self.payment_service.forfeit_deposit(booking.deposit)
        return Response(
            {"id": str(deposit.id), "status": deposit.status, "amount": str(deposit.amount)}
        )

    @action(detail=True, methods=["post"], url_path="invoice/pay")
    def pay_invoice(self, request, pk=None):
        booking = self.get_object()
        method = request.data.get("method", "card")
        if booking.customer != request.user and request.user.role not in (
            request.user.Role.ADMIN,
            request.user.Role.MANAGER,
        ):
            return Response(
                {"detail": "Not allowed to pay for this booking."}, status=status.HTTP_403_FORBIDDEN
            )

        invoice = getattr(booking, "invoice", None)
        if not invoice:
            invoice = self.booking_service.build_invoice(booking)["invoice"]
        invoice = self.payment_service.pay_invoice(invoice, method)
        return Response({"id": str(invoice.id), "status": "paid", "method": invoice.method})

    @action(detail=True, methods=["get"], url_path="quote")
    def pricing_quote(self, request, pk=None):
        booking = self.get_object()
        quote = self.booking_service.pricing_service.quote(
            booking.car, booking.start_date, booking.end_date
        )
        return Response(quote)

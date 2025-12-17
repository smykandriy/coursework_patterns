from rest_framework import permissions, viewsets
from rest_framework.response import Response
from django.db.models import Q

from apps.common.permissions import IsManagerOrAdmin

from .models import Car
from .serializers import CarSerializer


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]
        return [IsManagerOrAdmin()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = self._apply_filters(queryset, request)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def _apply_filters(self, queryset, request):
        params = request.query_params
        if make := params.get("make"):
            queryset = queryset.filter(make__icontains=make)
        if model := params.get("model"):
            queryset = queryset.filter(model__icontains=model)
        if car_type := params.get("type"):
            queryset = queryset.filter(type__iexact=car_type)
        if status := params.get("status"):
            queryset = queryset.filter(status=status)
        if year_min := params.get("year_min"):
            queryset = queryset.filter(year__gte=year_min)
        if year_max := params.get("year_max"):
            queryset = queryset.filter(year__lte=year_max)
        if search := params.get("search"):
            queryset = queryset.filter(Q(model__icontains=search) | Q(make__icontains=search))
        return queryset.order_by("make", "model", "year")

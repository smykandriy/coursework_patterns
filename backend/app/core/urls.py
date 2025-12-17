from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.schemas import get_schema_view


def healthcheck_view(_request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", healthcheck_view, name="healthcheck"),
    path("api/schema/", get_schema_view(title="Car Rental API"), name="api-schema"),
    path("api/auth/", include("apps.users.urls")),
    path("api/cars/", include("apps.cars.urls")),
    path("api/bookings/", include("apps.bookings.urls")),
    path("api/pricing/", include("apps.pricing.urls")),
    path("api/reports/", include("apps.reports.urls")),
]

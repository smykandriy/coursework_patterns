from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def healthcheck_view(_request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", healthcheck_view, name="healthcheck"),
    path("api/reports/", include("apps.reports.urls")),
    path("api/", include("apps.common.urls")),
]

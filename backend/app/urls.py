from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("api/auth/", include("app.apps.users.urls")),
    path("api/", include("app.apps.cars.urls")),
    path("api/", include("app.apps.pricing.urls")),
    path("api/", include("app.apps.bookings.urls")),
    path("api/", include("app.apps.payments.urls")),
    path("api/", include("app.apps.reports.urls")),
]

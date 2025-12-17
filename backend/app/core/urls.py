from django.contrib import admin
from django.urls import include, path

from core.views import health_check

api_urlpatterns = [
    path("health/", health_check, name="health"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns)),
]

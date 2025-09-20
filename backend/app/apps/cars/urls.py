from __future__ import annotations

from rest_framework.routers import DefaultRouter

from app.apps.cars.views import CarViewSet

router = DefaultRouter()
router.register(r"cars", CarViewSet, basename="car")

urlpatterns = router.urls

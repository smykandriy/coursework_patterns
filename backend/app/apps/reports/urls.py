from django.urls import path

from .views import reports_placeholder

urlpatterns = [
    path("", reports_placeholder, name="reports-placeholder"),
]

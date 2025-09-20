from django.contrib import admin

from app.apps.cars.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("make", "model", "year", "status")
    list_filter = ("status", "year")
    search_fields = ("make", "model", "vin")

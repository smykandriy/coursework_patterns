from django.contrib import admin

from app.apps.bookings.models import Booking, Deposit, Fine, Invoice


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "car", "customer", "start_date", "end_date", "status")
    list_filter = ("status", "start_date")
    search_fields = ("car__make", "customer__user__email")


admin.site.register(Deposit)
admin.site.register(Fine)
admin.site.register(Invoice)

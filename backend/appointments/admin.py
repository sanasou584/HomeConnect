from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "client", "provider", "date", "time_slot", "total_price", "status")
    list_filter = ("status", "date")
    search_fields = ("client__username", "provider__username", "service__name", "address")
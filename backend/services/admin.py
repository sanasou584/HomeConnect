from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "provider", "category", "pricing_type", "price", "base_city", "is_active")
    list_filter = ("category", "pricing_type", "is_active")
    search_fields = ("name", "provider__username", "base_city")
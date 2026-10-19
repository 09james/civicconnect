"""Django admin integration for service categories and requests."""

from django.contrib import admin

from .models import Category, ServiceRequest


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin list view for service categories."""

    search_fields = ("name",)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    """Admin list view for citizen requests."""

    list_display = ("id", "category", "citizen", "location", "status", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("location", "description", "citizen__username")
    readonly_fields = ("created_at", "updated_at", "resolved_at")

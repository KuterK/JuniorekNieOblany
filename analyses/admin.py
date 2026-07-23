from django.contrib import admin

from .models import Analysis


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "language", "status", "rating", "created_at")
    list_filter = ("status", "rating", "language")
    search_fields = ("title", "owner__username")
    readonly_fields = ("id", "created_at", "updated_at")

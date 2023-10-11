from django.contrib import admin
from apps.journey.models import Journey


# Register your models here.
@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "created_at", "updated_at")
    search_fields = ("title", "description")
    ordering = ("id",)

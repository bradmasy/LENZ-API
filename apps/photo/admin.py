from django.contrib import admin
from apps.photo.models import Photo

# Register your models here.
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "photo",
        "description",
        "active",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "id",
        "user",
        "photo",
        "description",
        "active",
        "created_at",
        "updated_at",
    )
    ordering = ("user",)
    list_filter = ()

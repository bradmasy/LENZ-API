from django.contrib import admin
from apps.journey.models import Journey, PhotoAlbumJourney


# Register your models here.
@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "created_at", "updated_at")
    search_fields = ("title", "description")
    ordering = ("id",)


@admin.register(PhotoAlbumJourney)
class PhotoAlbumJourneyAdmin(admin.ModelAdmin):
    list_display = ("id", "journey_id", "photo_album_id", "created_at", "updated_at")
    search_fields = ("journey_id", "photo_album_id")
    ordering = ("id",)

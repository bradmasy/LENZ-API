from django.contrib import admin
from apps.photo_album.models import PhotoAlbum


@admin.register(PhotoAlbum)
class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "created_at",
        "updated_at",
        "active",
    )

    search_fields = (
        "id",
        "title",
        "description",
        "created_at",
        "updated_at",
    )

    ordering = ("id",)
    list_filter = ()

from django.urls import path
from apps.photo_album.views import (
    PhotoAlbumsView,
    PhotoAlbumCreateView,
    PhotoAlbumByIDView,
)

urlpatterns = [
    path("photo-albums", PhotoAlbumsView.as_view(), name="photo-album-list"),
    path(
        "photo-album-create", PhotoAlbumCreateView.as_view(), name="photo-album-create"
    ),
    path("photo-album/<int:id>", PhotoAlbumByIDView.as_view(), name="photo-album-id"),
]

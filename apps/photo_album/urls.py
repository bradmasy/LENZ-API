from django.urls import path
from apps.photo_album.views import PhotoAlbumsView, PhotoAlbumCreateView

urlpatterns = [
    path("photo-albums", PhotoAlbumsView.as_view(), name="photo-album-list"),
    path(
        "photo-album-create", PhotoAlbumCreateView.as_view(), name="photo-album-create"
    ),
]

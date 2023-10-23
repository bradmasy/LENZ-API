from django.urls import path
from apps.photo_album.views import PhotoAlbumsView, PhotoAlbumCreateView, PhotoAlbumEditView

urlpatterns = [
    path("photo-album", PhotoAlbumsView.as_view(), name="photo-album-list"),
    path("photo-album/<int:pk>", PhotoAlbumsView.as_view(), name="photo-album-edit")
]

from django.urls import path
from .views import PhotoView, PhotoAlbumPhotoView, TagView

urlpatterns = [
    path("photo", PhotoView.as_view(), name="photo"),
    path("photo/<int:pk>", PhotoView.as_view(), name="photo-by-id"),
    path("photo-album-photo", PhotoAlbumPhotoView.as_view(), name="photo-album-photo"),
    path(
        "photo-album-photo/<int:pk>",
        PhotoAlbumPhotoView.as_view(),
        name="photo-album-photo-by-id",
    ),
    path("tag", TagView.as_view(), name="tag"),
]

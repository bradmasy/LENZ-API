from django.urls import path
from .views import (
    PhotoView,
    PhotoUpload,
    PhotoViewByID,
    PhotoAlbumPhotoCreateView,
    PhotoAlbumPhotoByIDView,
    PhotoAlbumPhotosView,
    PhotoAlbumPhotoView
)

urlpatterns = [
    path("photo", PhotoView.as_view(), name="photo"),
    path("photo/<int:id>", PhotoView.as_view(), name="photo-by-id"),
    path("photo-album-photo", PhotoAlbumPhotoView.as_view(), name ="photo-album-photo"),
    path("photo-album-photo/<int:pk>", PhotoAlbumPhotoView.as_view(), name ="photo-album-photo-by-id")

]

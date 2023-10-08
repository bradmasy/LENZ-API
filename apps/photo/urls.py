from django.urls import path
from .views import PhotoView, PhotoUpload, PhotoViewByID, PhotoAlbumPhotoCreateView

urlpatterns = [
    path("photos", PhotoView.as_view(), name="photos"),
    path("photo-upload", PhotoUpload.as_view(), name="photo-upload"),
    path("photo/<int:id>", PhotoViewByID.as_view(), name="photo-id"),
    path(
        "photo-album-photo",
        PhotoAlbumPhotoCreateView.as_view(),
        name="photo-album-photos",
    ),
]

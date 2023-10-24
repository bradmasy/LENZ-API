from django.urls import path
from apps.photo_album.views import (
    PhotoAlbumsView,
)

urlpatterns = [
    path("photo-album", PhotoAlbumsView.as_view(), name="photo-album"),
    path("photo-album/<int:pk>", PhotoAlbumsView.as_view(), name="photo-album-pk"),
]

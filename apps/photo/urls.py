from django.urls import path
from .views import PhotoView, PhotoUpload, PhotoViewByID

urlpatterns = [
    path("photos", PhotoView.as_view(), name="photos"),
    path("photo-upload",PhotoUpload.as_view(), name="photo-upload"),
    path("photo/<int:id>", PhotoViewByID.as_view(), name="photo-id"),
]
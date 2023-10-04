from django.urls import path
from .views import PhotosView

urlpatterns = [
    path("photos", PhotosView.as_view(), name="photos"),
]
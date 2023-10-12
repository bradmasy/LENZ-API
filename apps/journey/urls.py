from django.urls import path
from apps.journey.views import (
    JourneyListView,
    JourneyCreateView,
    PhotoAlbumJourneyListView,
    PhotoAlbumJourneyCreateView,
)

urlpatterns = [
    path("journeys", JourneyListView.as_view(), name="journey-list"),
    path("journey-create", JourneyCreateView.as_view(), name="journey-create"),
    path(
        "photo-album-journeys",
        PhotoAlbumJourneyListView.as_view(),
        name="photo-album-journey-list",
    ),
    path(
        "photo-album-journey-create",
        PhotoAlbumJourneyCreateView.as_view(),
        name="photo-album-journey-create",
    ),
]

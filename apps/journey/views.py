from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.journey.serializers import JourneySerializer, PhotoAlbumJourneySerializer
from apps.journey.models import Journey, PhotoAlbumJourney


class JourneyListView(generics.ListCreateAPIView):
    """View all the journeys in the database

    Args:
        generics (generics): ListCreateAPIView
    """

    permission_classes = [IsAuthenticated]
    serializer_class = JourneySerializer
    queryset = Journey.objects.get_active_journeys()


class JourneyCreateView(generics.CreateAPIView):
    """View to create a new journey.

    Args:
        generics (generics): CreateAPIView

    Returns:
        CreateAPIView: Returns the newly created journey
    """

    permission_classes = [IsAuthenticated]
    serializer_class = JourneySerializer

    def get_queryset(self):
        id = self.kwargs.get("id", None)
        queryset = Journey.objects.get_by_id(id=id)
        return queryset


class PhotoAlbumJourneyListView(generics.ListCreateAPIView):
    """View all the photo albums in the database

    Args:
        generics (generics): ListCreateAPIView
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PhotoAlbumJourneySerializer
    queryset = PhotoAlbumJourney.objects.all()


class PhotoAlbumJourneyCreateView(generics.CreateAPIView):
    """View to create a new photo album.

    Args:
        generics (generics): CreateAPIView

    Returns:
        CreateAPIView: Returns the newly created photo album
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PhotoAlbumJourneySerializer

    def get_queryset(self):
        id = self.kwargs.get("id", None)
        queryset = PhotoAlbumJourney.objects.get_by_id(id=id)
        return queryset

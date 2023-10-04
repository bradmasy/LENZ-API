from rest_framework import generics
from apps.photo.serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticated
from apps.photo.models import Photo

class PhotoView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer
    
    # make this related interests photos
    queryset = Photo.objects.all()


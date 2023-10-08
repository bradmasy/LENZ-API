from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.photo_album.models import PhotoAlbum
from apps.photo_album.serializers import PhotoAlbumSerializer, PhotoAlbumCreateSerializer

# Create your views here.
class PhotoAlbumsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoAlbumSerializer
    queryset = PhotoAlbum.objects.all()
    
    
class PhotoAlbumCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoAlbumCreateSerializer
    
        
        
    

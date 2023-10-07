from rest_framework import generics
from apps.photo.serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticated
from apps.photo.models import Photo
from apps.photo.serializers import PhotoUploadSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from apps.user.models import User
import io


class PhotoView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer

    # make this related interests photos
    queryset = Photo.objects.all()


class PhotoUpload(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)
    serializer_class = PhotoUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = PhotoUploadSerializer(data=request.data)
        
        try:
            if serializer.is_valid(raise_exception=True):
                photo = serializer.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(PhotoSerializer(photo).data, status=status.HTTP_201_CREATED)

class PhotoViewByID(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer
    
    def get_queryset(self):
        id = self.kwargs.get('id', None)  
        print("args ", self.kwargs)
        queryset = Photo.objects.by_id(id)
        return queryset
from rest_framework import generics
from apps.photo.serializers import PhotoSerializer
from rest_framework.permissions import IsAuthenticated
from apps.photo.models import Photo, PhotoAlbumPhoto
from apps.photo.serializers import PhotoUploadSerializer, PhotoAlbumPhotoSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.db import transaction

# class PhotoView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PhotoSerializer

#     # make this related interests photos
#     queryset = Photo.objects.all()


class PhotoView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            with transaction.atomic():
                serializer.is_valid(raise_exception=True)
                serializer.save()
                response_data = {
                    "message": "Successfully Created a Photo",
                    "photo": serializer.data,  # Use serializer.data to get the serialized representation
                }
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "PUT Request Successful", "photo": serializer.data},
            status=status.HTTP_200_OK,
        )

    def patch(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                serializer = self.get_serializer(
                    instance, data=request.data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "message": "Successfully Updated Photo",
                "photo_album": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                serializer = self.get_serializer(instance)
                serializer.delete(instance)
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "message": "Photo Album Successfully Deleted",
                "photo": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


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
        id = self.kwargs.get("id", None)
        queryset = Photo.objects.by_id(id)
        return queryset


class PhotoAlbumPhotoCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoAlbumPhotoSerializer


class PhotoAlbumPhotoByIDView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoAlbumPhotoSerializer

    def get_queryset(self):
        id = self.kwargs.get("id", None)
        queryset = PhotoAlbumPhoto.objects.get_by_album_id(id=id)
        return queryset


class PhotoAlbumPhotosView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoAlbumPhotoSerializer

    def get_queryset(self):
        queryset = PhotoAlbumPhoto.objects.all()
        return queryset

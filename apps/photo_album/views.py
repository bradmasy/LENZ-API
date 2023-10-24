from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.photo_album.models import PhotoAlbum
from apps.photo_album.serializers import PhotoAlbumSerializer
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status


class PhotoAlbumsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoAlbumSerializer
    queryset = PhotoAlbum.objects.all()

    def get(self, request, *args, **kwargs):
        """GET Request for Photo Albums.

        Args:
            request (request): the request data

        Returns:
            Response: on success, all the photo albums.
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """POST Method for Photo Album.

        Args:
            request (request): the request data

        Returns:
            Response: on success, the created photo album.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            with transaction.atomic():
                serializer.is_valid(raise_exception=True)
                serializer.save()
                response_data = {
                    "message": "Successfully Created Photo Album",
                    "photo_album": serializer.data,  # Use serializer.data to get the serialized representation
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
            {"message": "PUT Request Successful", "photo_album": serializer.data},
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
                response_data = {
                    "message": "Successfully Updated Photo Album",
                    "photo_album": serializer.data,
                }
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status=status.HTTP_200_OK)

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
                "photo_album": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

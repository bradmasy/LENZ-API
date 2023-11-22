import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.photo.models import Photo, PhotoAlbumPhoto, Tag
from apps.photo.serializers import (
    PhotoAlbumPhotoSerializer,
    PhotoSerializer,
    BasicPhotoSerializer,
    TagSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from libs.custom_limit_offset_pagination import CustomLimitOffsetPagination


class PhotoView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
    pagination_class = CustomLimitOffsetPagination
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        id = kwargs.get("pk", None)

        query_params = request.query_params

        if query_params:
            queries = {
                "title": query_params.get("title", ".*"),
                "description": query_params.get("description", ".*"),
                "from_date": query_params.get(
                    "from_date",
                    (datetime.datetime.now() - datetime.timedelta(days=5 * 365)).date(),
                ),
                "to_date": query_params.get("to_date", datetime.datetime.now().date()),
                "tags": query_params.get("tags", []),
                "limit": query_params.get("limit", 25),
                "offset": query_params.get("offset", 0),
            }
            queryset = Photo.objects.by_search_query(queries)
            serializer = BasicPhotoSerializer(queryset, many=True)

        else:
            # Signifies querying a specific photo: "/photo/123" etc
            if id is not None:
                queryset = Photo.objects.get(id=id)
                serializer = BasicPhotoSerializer(queryset, many=False)
            else:
                queryset = self.get_queryset()
                serializer = BasicPhotoSerializer(queryset, many=True)

        return self.pagination_class().get_paginated_response(
            Photo, request, serializer.data
        )

    def get(self, request, *args, **kwargs):
        try:
            response = self.list(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        return response

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)

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
                "photo": serializer.data,
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


class PhotoViewByID(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer

    def get_queryset(self):
        id = self.kwargs.get("id", None)
        queryset = Photo.objects.by_id(id)
        return queryset


class PhotoAlbumPhotoView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoAlbumPhotoSerializer
    queryset = PhotoAlbumPhoto.objects.all()
    pagination_class = CustomLimitOffsetPagination
    # parser_classes = (MultiPartParser, FormParser)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return self.pagination_class().get_paginated_response(
            model=PhotoAlbumPhoto, request=request, data=serializer.data
        )

    def get(self, request, *args, **kwargs):
        try:
            response = self.list(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        return response

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            with transaction.atomic():
                serializer.is_valid(raise_exception=True)
                serializer.save()
                response_data = {
                    "message": "Successfully Created a Photo Album Photo",
                    "photo_album_photo": serializer.data,  # Use serializer.data to get the serialized representation
                }
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status=status.HTTP_201_CREATED)

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
                "photo_album_photo": serializer.data,
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
                "message": "Photo Album Photo Successfully Deleted",
                "photo_album_photo": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


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


class TagView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            with transaction.atomic():
                serializer.is_valid(raise_exception=True)
                tag = serializer.save()
                photo = BasicPhotoSerializer(
                    Photo.objects.get(id=request.data.get("photo_id"))
                ).data
                print(f"the tag: {tag}")
                response_data = {
                    "message": "Successfully Added Tag",
                    "data": {"Tag": f"{tag}", "Photo": f"{photo.get('id')}"},
                }

        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class RecoverPhoto(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PhotoSerializer
    
    def post(self, request, *args, **kwargs):
        
        try:
            with transaction.atomic():
                
        except Exception as e:
            return Response({"error":f"{e}"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Photo has been recovered"})
            
    

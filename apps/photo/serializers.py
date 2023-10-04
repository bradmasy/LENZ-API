from rest_framework import serializers
from .models import Photo, PhotoAlbumPhoto


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("id", "title", "description", "image", "created_at", "updated_at")

    
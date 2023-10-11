from rest_framework import serializers
from apps.photo.models import Photo, PhotoAlbumPhoto
from apps.photo_album.models import PhotoAlbum
from apps.user.models import User
from django.db import transaction


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("id", "description", "title", "photo", "created_at", "updated_at")


class PhotoUploadSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    photo = serializers.ImageField()
    description = serializers.CharField()
    active = serializers.BooleanField()
    title = serializers.CharField()

    def create(self, validated_data):
        validated_data["user_id"] = User.objects.get(id=validated_data["user_id"]).id
        image_bytes = validated_data["photo"].read()
        photo = Photo.objects.create(
            user_id=User.objects.get(id=validated_data["user_id"]),
            photo=image_bytes,
            description=validated_data["description"],
            active=validated_data["active"],
            title=validated_data["title"],
        )

        return photo

    def validate(self, attrs, raise_exception=False):
        # add validations
        return attrs

    class Meta:
        model = Photo
        fields = (
            "id",
            "user_id",
            "title",
            "description",
            "active",
            "photo",
            "created_at",
            "updated_at",
        )


class PhotoAlbumPhotoSerializer(serializers.ModelSerializer):
    photo_id = serializers.PrimaryKeyRelatedField(
        queryset=Photo.objects.all(), required=True
    )
    photo_album_id = serializers.PrimaryKeyRelatedField(
        queryset=PhotoAlbum.objects.all(), required=True
    )

    def validate(self, attrs):
        if not attrs["photo_album_id"]:
            raise serializers.ValidationError("Photo album id is required")
        elif not attrs["photo_id"]:
            raise serializers.ValidationError("Photo id is required")
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            photo_album_photo = PhotoAlbumPhoto.objects.create(**validated_data)

        return photo_album_photo

    class Meta:
        model = PhotoAlbumPhoto
        fields = ("id", "photo_album_id", "photo_id")
        unique_together = ("photo_album_id", "photo_id")

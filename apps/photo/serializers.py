from rest_framework import serializers
from apps.photo.models import Photo, PhotoAlbumPhoto
from apps.photo_album.models import PhotoAlbum
from apps.user.models import User
from django.db import transaction


class BasicPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("id", "description", "title", "photo", "created_at", "updated_at")


class PhotoSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    photo = serializers.ImageField()
    description = serializers.CharField()
    active = serializers.BooleanField()
    title = serializers.CharField()

    class Meta:
        model = Photo
        fields = (
            "id",
            "user_id",
            "description",
            "title",
            "photo",
            "active",
            "created_at",
            "updated_at",
        )

    def to_representation(self, instance):
        serialized = BasicPhotoSerializer(instance).data
        return serialized

    def create(self, validated_data):
        image_bytes = validated_data["photo"].read()
        photo = Photo.objects.create(
            user_id=validated_data["user_id"],
            photo=image_bytes,
            description=validated_data["description"],
            active=validated_data["active"],
            title=validated_data["title"],
        )

        return photo

    def delete(self, instance):
        instance.delete()

    def update(self, instance, validated_data):
        if validated_data.get("photo", None) is not None:
            validated_data["photo"] = validated_data["photo"].read()

        return super().update(instance, validated_data)


class PhotoAlbumPhotoSerializer(serializers.ModelSerializer):
    photo_id = serializers.PrimaryKeyRelatedField(
        queryset=Photo.objects.all(), required=True
    )
    photo_album_id = serializers.PrimaryKeyRelatedField(
        queryset=PhotoAlbum.objects.all(), required=True
    )

    photo = BasicPhotoSerializer(read_only=True)

    def to_representation(self, instance):
        photo = Photo.objects.get(id=instance.photo_id.id)
        instance.photo = photo

        return super().to_representation(instance)

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
        fields = ("id", "photo_id", "photo_album_id", "photo")
        unique_together = ("photo_album_id", "photo_id")

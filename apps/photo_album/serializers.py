from rest_framework import serializers
from apps.photo_album.models import PhotoAlbum
from apps.photo.serializers import PhotoSerializer, PhotoAlbumPhotoSerializer
from apps.photo.models import PhotoAlbumPhoto
from apps.journey.models import PhotoAlbumJourney
from apps.user.models import User
from django.db import transaction


class PhotoAlbumSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    photos = PhotoSerializer(many=True, read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )

    class Meta:
        model = PhotoAlbum
        fields = (
            "id",
            "user_id",
            "title",
            "photos",
            "description",
            "created_at",
            "updated_at",
            "active",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        photos = PhotoAlbumPhoto.objects.filter(photo_album_id=instance.id)
        photo_serializer = PhotoAlbumPhotoSerializer(photos, many=True)
        representation[
            "photos"
        ] = photo_serializer.data  # Update the 'photos' key in the representation
        return representation

    def validate(self, attrs):
        return super().validate(attrs)

    def delete_related_objects(self, instance):
        photo_album_journeys = PhotoAlbumJourney.objects.filter(
            photo_album_id=instance.id
        )
        photo_album_journeys.delete()

    def delete(self, instance):
        self.delete_related_objects(instance)
        instance.delete()

    def create(self, validated_data):
        with transaction.atomic():
            photo_album = PhotoAlbum.objects.create(
                user_id=validated_data["user_id"],
                title=validated_data["title"],
                description=validated_data["description"],
                active=True,  # always active on creation
            )

        return photo_album


class PhotoAlbumCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True
    )
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    photos = PhotoSerializer(many=True, read_only=True)

    def validate(self, attrs):
        if not attrs["user_id"]:
            raise serializers.ValidationError("User id is required")
        elif not attrs["title"]:
            raise serializers.ValidationError("Title is required")
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            photo_album = PhotoAlbum.objects.create(
                user_id=validated_data["user_id"],
                title=validated_data["title"],
                description=validated_data["description"],
                active=True,  # always active on creation
            )

        return photo_album

    class Meta:
        model = PhotoAlbum
        fields = (
            "id",
            "user_id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "photos",
            "active",
        )


class PhotoAlbumEditSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    photos = PhotoSerializer(many=True, read_only=True)
    id = serializers.IntegerField(required=True)

    class Meta:
        model = PhotoAlbum
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "photos",
            "active",
        )

    def validate(self, attrs):
        print("validate")
        print(attrs)
        return super().validate(attrs)

    def update(self, instance, validated_data):
        print("hello")
        return super().update(instance, validated_data)

from rest_framework import serializers
from apps.photo.models import Photo, PhotoAlbumPhoto
from apps.user.models import User


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("id", "description", "photo", "created_at", "updated_at")


class PhotoUploadSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    photo = serializers.ImageField()
    description = serializers.CharField()
    active = serializers.BooleanField()

    def create(self, validated_data):
        validated_data["user_id"] = User.objects.get(id=validated_data["user_id"]).id
        image_bytes = validated_data["photo"].read()
        photo = Photo.objects.create(
            user_id=User.objects.get(id=validated_data["user_id"]),
            photo=image_bytes,
            description=validated_data["description"],
            active=validated_data["active"],
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
            "description",
            "active",
            "photo",
            "created_at",
            "updated_at",
        )

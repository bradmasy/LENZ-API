from rest_framework import serializers
from apps.photo.models import Photo, PhotoAlbumPhoto, Tag
from apps.photo_album.models import PhotoAlbum
from apps.user.models import User
from django.db import transaction


class BasicPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = (
            "id",
            "description",
            "title",
            "latitude",
            "longitude",
            "photo",
            "created_at",
            "updated_at",
        )


class PhotoSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    photo = serializers.ImageField()
    description = serializers.CharField()
    active = serializers.BooleanField()
    title = serializers.CharField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)

    class Meta:
        model = Photo
        fields = (
            "id",
            "user_id",
            "description",
            "title",
            "photo",
            "active",
            "longitude",
            "latitude",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        id = attrs.get("id", None)
        photo = attrs.get("photo", None)
        user_id = attrs.get("user_id", None)
        description = attrs.get("description", "")
        active = attrs.get("active", True)
        title = attrs.get("title", None)
        latitude = attrs.get("latitude", None)
        longitude = attrs.get("longitude", None)

        print(f"validating... {attrs}")

        if not user_id:
            raise Exception("User ID must be in request.")

        validated_dict = (
            {
                "photo": photo,
                "user_id": user_id,
                "description": description,
                "active": active,
                "title": title,
                "latitude": latitude,
                "longitude": longitude,
            }
            if photo is not None  # if there is a photo...
            else {
                "user_id": user_id,
                "description": description,
                "active": active,
                "title": title,
                "latitude": latitude,
                "longitude": longitude,
            }
        )

        validated_dict = (
            validated_dict
            if title is not None
            else {
                "user_id": user_id,
                "description": description,
                "active": active,
                "latitude": latitude,
                "longitude": longitude,
            }
        )

        if id:
            validated_dict["id"] = id

        return super().validate(validated_dict)

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
            latitude=validated_data["latitude"],
            longitude=validated_data["longitude"],
            title=validated_data["title"],
        )

        return photo

    def delete(self, instance):
        print(instance)
        instance.delete()

    def update(self, instance, validated_data):
        current_instance_data = BasicPhotoSerializer(instance).data
        attributes_list = list(current_instance_data.keys())

        for key, value in validated_data.items():
            if (
                key in attributes_list and key != "photo"
            ):  # photo needs to be handled separate.
                setattr(instance, key, value)

        if "photo" in validated_data:
            instance.photo = validated_data["photo"].read()

        instance.save()
        return instance


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


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    photo_id = serializers.PrimaryKeyRelatedField(
        queryset=Photo.objects.all(), required=True
    )

    def create(self, validated_data):
        tag, id = Tag.objects.get_or_create(name=validated_data.get("name"))
        photo = Photo.objects.get(id=validated_data.get("photo_id").id)
        photo.tags.add(tag)

        return tag

    def validate(self, attrs):
        return super().validate(attrs)

    def save(self, *args, **kwargs):
        # should create a relationship entity after creating the tag
        return super().save(*args, **kwargs)

    class Meta:
        model = Tag
        fields = ("id", "name", "photo_id")
        unique = "name"

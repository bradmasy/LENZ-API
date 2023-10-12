from rest_framework import serializers
from apps.journey.models import Journey, PhotoAlbumJourney


class PhotoAlbumJourneySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if not attrs["photo_album_id"]:
            raise serializers.ValidationError("PhotoAlbumID is required")
        if not attrs["journey_id"]:
            raise serializers.ValidationError("JourneyID is required")
        return attrs

    def create(self, validated_data):
        return PhotoAlbumJourney.objects.create(**validated_data)

    class Meta:
        model = PhotoAlbumJourney
        fields = ("id", "photo_album_id", "journey_id", "created_at", "updated_at")


class JourneySerializer(serializers.ModelSerializer):
    photo_albums = PhotoAlbumJourneySerializer(many=True, read_only=True)

    def validate(self, attrs):
        if not attrs["title"]:
            raise serializers.ValidationError("Title is required")
        if not attrs["user_id"]:
            raise serializers.ValidationError("UserID is required")
        return attrs

    def create(self, validated_data):
        return Journey.objects.create(**validated_data)

    class Meta:
        model = Journey
        fields = (
            "id",
            "title",
            "photo_albums",
            "description",
            "user_id",
            "created_at",
            "updated_at",
            "active",
            "size",
        )

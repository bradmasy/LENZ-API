from rest_framework import serializers
from apps.journey.models import Journey


class JourneySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        pass
    def create(self, validated_data):
        pass
    class Meta:
        model = Journey
        fields = "__all__"
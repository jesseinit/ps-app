from rest_framework import serializers

from .models import Images, Trips


class UserScoreSerializer(serializers.Serializer):
    """Serializers a name field for testing our API Views"""

    quality_score = serializers.CharField(max_length=10)


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"


class TripsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trips
        fields = "__all__"

from rest_framework import serializers


class UserScoreSerializer(serializers.Serializer):
    """Serializers a name field for testing our API Views"""

    quality_score = serializers.CharField(max_length=10)

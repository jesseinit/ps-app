from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers, models
from rest_framework import status

from .serializers import ImagesSerializer
from django.db.models import F
from django.db.models.functions import Sqrt, Power

# Create your views here.

# Get User Score
# Get User Score
# Get User Score


class UserScoreView(APIView):
    """Get User Score API"""

    serializer_class = serializers.UserScoreSerializer

    def get(self, request, user_id, *args, **kwargs):
        """Returns a user score"""

        return Response({"user_score": 234})


class ImageSearchView(APIView):

    def get(self, request, search_param):

        # Check if the parameter is an ID (numeric)
        if search_param.isdigit():
            image_id = int(search_param)
            image = models.Images.objects.filter(id=image_id)
            serializer = ImagesSerializer(image)
            return Response(serializer.data)

        try:
            lat, lon = map(float, search_param.split(","))
        except ValueError:
            return Response(
                {"error": "Invalid search parameter format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find 10 nearest images based on Euclidean distance
        images = models.Images.objects.annotate(
            distance=Sqrt(Power(F("lat") - lat, 2) + Power(F("lon") - lon, 2))
        ).order_by("distance")[:10]
        serializer = ImagesSerializer(images, many=True)
        return Response(serializer.data)

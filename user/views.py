from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers, models
from rest_framework import status

from .serializers import ImagesSerializer
from django.db.models import F, Sum, Case, IntegerField, When, Count
from django.db.models.functions import Sqrt, Power
import math
from datetime import timedelta

# Create your views here.


def haversine(lat1, lon1, lat2, lon2):
    # Calculate the distance between two latitude/longitude points
    R = 6371  # Radius of the Earth in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in km


class UserScoreView(APIView):
    """Get User Score API"""

    serializer_class = serializers.UserScoreSerializer

    def get(self, request, user_id, *args, **kwargs):
        """Returns a user score"""
        # Calculate points based on whether steps have photos
        trips_with_photo_points = models.Trips.filter(user_id=user_id).objects.annotate(
            step_photo_points=Sum(
                Case(
                    When(steps__media__path__isnull=False, then=2),  # Step with photos
                    default=1,  # Step without photos
                    output_field=IntegerField(),
                )
            )
        )

        trips_with_text_points = trips_with_photo_points.annotate(
            step_text_points=Sum(
                Case(
                    When(steps__description__isnull=False, then=1),  # Step with text
                    default=0,
                    output_field=IntegerField(),
                )
            )
        )

        for trip in models.Trips.objects.all():
            steps = trip.steps.order_by("start_time")
            total_distance_points = 0

            for i in range(1, len(steps)):
                prev_step = steps[i - 1]
                current_step = steps[i]
                distance = haversine(
                    prev_step.location.lat,
                    prev_step.location.lon,
                    current_step.location.lat,
                    current_step.location.lon,
                )
                total_distance_points += int(distance / 100)  # 1 point per 100 km

            trip.distance_points = total_distance_points

        trips_with_duration_points = trips_with_text_points.annotate(
            duration_points=Sum(
                Case(
                    When(
                        end_date__isnull=False,
                        start_date__isnull=False,
                        then=(F("end_date") - F("start_date")) / timedelta(days=7),
                    ),
                    default=0,
                    output_field=IntegerField(),
                )
            )
        )

        trips_with_total_points = trips_with_duration_points.annotate(
            total_trip_points=F("step_photo_points")
            + F("step_text_points")
            + F("duration_points")
            + F("distance_points")
        )

        for trip in trips_with_total_points:
            print(f"Trip: {trip.name}, Total Points: {trip.total_trip_points}")

            # Count distinct locations based on name and detail for each user
        users_with_location_diversity = models.Users.objects.annotate(
            location_count=Count("trips__steps__location__name", distinct=True)
        )

        # Calculate points based on location diversity (1 point per 5 different locations)
        for user in users_with_location_diversity:
            location_diversity_points = user.location_count // 5
            print(
                f"User: {user.username}, Location Diversity Points: {location_diversity_points}"
            )

        return Response({"user_score": 234})


class ImageSearchView(APIView):

    def get(self, request, search_param):

        # Check if the parameter is an ID (numeric)
        if search_param.isdigit():
            image_id = int(search_param)
            # Filter has been used here because apparently IDs on the table aren't unique
            image = models.Images.objects.filter(id=image_id)
            serializer = ImagesSerializer(image, many=True)
            return Response(serializer.data)

        try:
            lat, lon = map(float, search_param.split(","))
        except ValueError:
            return Response(
                {"error": "Invalid search parameter format."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find 10 nearest images based on Euclidean distance
        images = (
            models.Images.objects.exclude(lat__isnull=True, lon__isnull=True)
            .annotate(
                distance=Sqrt(Power(F("lat") - lat, 2) + Power(F("lon") - lon, 2))
            )
            .order_by("distance")[:10]
        )
        serializer = ImagesSerializer(images, many=True)
        return Response(serializer.data)

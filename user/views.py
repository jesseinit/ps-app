from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers, models
from rest_framework import status

from .serializers import ImagesSerializer
from django.db.models import (
    F,
    Sum,
    Case,
    IntegerField,
    When,
    ExpressionWrapper,
    FloatField,
    Value,
    Count,
    Q,
    Func,
    Window,
    Subquery,
    OuterRef,
)
from django_cte import With

from django.db.models.functions import Sqrt, Power, Extract, Lag, Coalesce

from django.contrib.postgres.search import SearchQuery

from user.factories import UsersFactory, TripsFactory, StepsFactory, ImagesFactory


# Define a custom Func for using the haversine function
class Haversine(Func):
    function = "haversine"
    template = "%(function)s(%(expressions)s)"


class UserScoreView(APIView):
    """Get User Score API"""

    serializer_class = serializers.UserScoreSerializer

    # @transaction.atomic
    def get(self, request, user_id, *args, **kwargs):
        """Returns a user score"""
        # Calculate points based on whether steps have photos

        # Figured out that this endpoint wasn't necesarily hanging or the connection timing out
        # the query was just very slow hence why we thought it hung.

        # Create 10 users, each with 30 trips
        # for _ in range(50):
        #     # ImagesFactory()
        #     #     # Create a user
        #     user = UsersFactory()
        #     for _ in range(50):
        #         trips = TripsFactory.create_batch(size=100, user=user)
        #         for trip in trips:
        #             StepsFactory.create_batch(size=20, trip=trip)

        step_cte = With(
            queryset=models.Steps.objects.filter(trip__user_id=user_id)
            .annotate(
                prev_lat=Window(
                    expression=Lag("location__lat", offset=1),
                    partition_by=F("trip_id"),
                    order_by=F("start_time").asc(),
                ),
                prev_lon=Window(
                    expression=Lag("location__lon", offset=1),
                    partition_by=F("trip_id"),
                    order_by=F("start_time").asc(),
                ),
            )
            .values(
                "id",
                "location__lat",
                "trip_id",
                "location__lon",
                "location__id",
                "prev_lat",
                "prev_lon",
            )
        )

        trips_with_distances = (
            step_cte.queryset()
            .annotate(
                distance_points=Case(
                    When(
                        prev_lat__isnull=False,
                        prev_lon__isnull=False,
                        then=Haversine(
                            F("prev_lat"),
                            F("prev_lon"),
                            F("location__lat"),
                            F("location__lon"),
                        )
                        / 100,  # Convert distance to points (1 point per 100 km)
                    ),
                    default=0,
                    output_field=FloatField(),
                )
            )
            .annotate(total_distance_points=Sum("distance_points"))
            .values("trip_id", "total_distance_points")
        )

        trips_query = (
            models.Trips.objects.filter(user_id=user_id)
            .with_cte(step_cte)
            .annotate(
                with_photo_points=Sum(
                    Case(
                        When(steps__main_media_item_path__isnull=False, then=2),
                        default=0,
                        output_field=IntegerField(),
                    )
                ),
                with_out_photo_points=Sum(
                    Case(
                        When(steps__main_media_item_path__isnull=True, then=1),
                        default=0,
                        output_field=IntegerField(),
                    )
                ),
                with_text_points=Sum(
                    Case(
                        When(steps__description__isnull=False, then=1),
                        default=0,
                        output_field=IntegerField(),
                    )
                ),
                # Count unique combinations of name and detail for each trip
                location_diversity_points=Count(
                    "steps__location",
                    distinct=True,
                    filter=Q(steps__location__name__isnull=False)
                    & Q(steps__location__detail__isnull=False)
                    & Q(steps__location__name=F("steps__location__detail")),
                ),
                # Calculate points based on unique location combinations
                diversity_points=F("location_diversity_points") / 5,
                duration_points=Sum(
                    Case(
                        When(
                            end_date__isnull=False,
                            start_date__isnull=False,
                            start_date__lt=F("end_date"),
                            then=ExpressionWrapper(
                                Extract(F("end_date") - F("start_date"), "days") / 7,
                                output_field=IntegerField(),
                            ),
                        ),
                        default=0,
                        output_field=IntegerField(),
                    )
                ),
                # Annotate distance points by joining with the CTE
                distance_points=Coalesce(
                    Subquery(
                        trips_with_distances.filter(trip_id=OuterRef("id")).values(
                            "total_distance_points"
                        )[:1],
                        output_field=IntegerField(),
                    ),
                    Value(0),
                ),
            )
        )

        total_distance_points = 0

        for trip in trips_query:
            total_distance_points += sum(
                [
                    trip.with_photo_points,
                    trip.with_out_photo_points,
                    trip.with_text_points,
                    trip.duration_points,
                    trip.diversity_points,
                    trip.distance_points,
                ]
            )

        # Takes 5seconds for 3500 trips, 69k steps
        data = serializers.UserScoreSerializer({"quality_score": total_distance_points})
        return Response(data.data)


class ImageSearchView(APIView):

    def get(self, request, search_param):

        # Check if the parameter is an ID (numeric)
        if search_param.isdigit():
            image_id = int(search_param)
            # Filter has been used here because apparently IDs on the table aren't unique
            image = models.Images.objects.filter(id=image_id).first()
            if not image:
                return Response({"message": "Image not found"}, status=404)
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
        images = (
            models.Images.objects.exclude(lat__isnull=True, lon__isnull=True)
            .annotate(
                distance=Sqrt(Power(F("lat") - lat, 2) + Power(F("lon") - lon, 2))
            )
            .order_by("distance")[:10]
        )
        serializer = ImagesSerializer(images, many=True)
        return Response(serializer.data)


class RelevantTripsView(APIView):

    def get(self, request, search_param):
        # Not Relevant but figured out that something this simple could have been a decent enough first iteration
        # The search query essentially parses the name and summary fields to postgres tsvector data type and performs the lookup on those

        # Added a GIN index on the search_vector for index lookups
        relevant_trips = models.Trips.objects.filter(
            search_vector=SearchQuery(search_param)
        ).order_by("-quality_score", "-likes")
        serializer = serializers.TripsSerializer(relevant_trips[:10], many=True)
        return Response(serializer.data)

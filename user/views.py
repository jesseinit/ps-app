from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers

# Create your views here.

# Get User Score
# Get User Score
# Get User Score


class UserScoreView(APIView):
    """Get User Score API"""

    # Define serializer fot this view
    serializer_class = serializers.UserScoreSerializer

    def get(self, request, user_id, *args, **kwargs):
        """Returns a user score"""

        return Response({"user_score": 234})

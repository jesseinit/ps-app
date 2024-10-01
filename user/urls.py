from django.urls import path
from . import views

urlpatterns = [
    path("user-score/<int:user_id>/", views.UserScoreView.as_view(), name="user-score")
]

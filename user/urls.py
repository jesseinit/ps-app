from django.urls import path
from . import views

urlpatterns = [
    path("user-score/<int:user_id>/", views.UserScoreView.as_view(), name="user-score"),
    path(
        "image-search/<str:search_param>/",
        views.ImageSearchView.as_view(),
        name="image-search",
    ),
]

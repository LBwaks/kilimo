from django.urls import path

from .views import LandDetailView, LandListView

urlpatterns = [
    path("", LandListView.as_view(), name="land"),
    path("land-details/<slug>", LandDetailView.as_view(), name="land-details"),
]

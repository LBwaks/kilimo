from django.urls import path

from .views import LandDetailView, LandListView,LandWizard

urlpatterns = [
    path("", LandListView.as_view(), name="land"),
    path("land-details/<slug>", LandDetailView.as_view(), name="land-details"),
    path("add-land/", LandWizard.as_view(), name="add-land")
]

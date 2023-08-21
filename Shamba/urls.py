from django.urls import path

from .views import LandDetailView, LandListView,LandWizard,LandUpdateView,LandDeleteView

urlpatterns = [
    path("", LandListView.as_view(), name="land"),
    path("land-details/<slug>", LandDetailView.as_view(), name="land-details"),
    path("land-update/<slug>", LandUpdateView.as_view(), name="land-update"),
    path("land-delete/<slug>", LandDeleteView.as_view(), name="land-delete"),
    path("add-land/", LandWizard.as_view(), name="add-land"),
]

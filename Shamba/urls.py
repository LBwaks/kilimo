from django.urls import path

from .views import (
    LandByCategory,
    LandDeleteView,
    LandDetailView,
    LandListView,
    LandUpdateView,
    LandWizard,
    MyBookmarks,
    MyLands,
    UsersLand,
    bookmark,
    LandCoordinateCreateView,
)

urlpatterns = [
    path("", LandListView.as_view(), name="land"),
    path("land-details/<slug>", LandDetailView.as_view(), name="land-details"),
    path("land-update/<slug>", LandUpdateView.as_view(), name="land-update"),
    path("land-delete/<slug>", LandDeleteView.as_view(), name="land-delete"),
    path("add-land/", LandWizard.as_view(), name="add-land"),
    path("bookmark/<slug>", bookmark, name="bookmark"),
    path("my-bookmarks/<username>", MyBookmarks.as_view(), name="my-bookmarks"),
    path("my-lands/", MyLands.as_view(), name="my-lands"),
    path("users-lands/<username>", UsersLand.as_view(), name="users-lands"),
    path("land-by-category/<slug>", LandByCategory.as_view(), name="land-category"),
    path("add-coordinates/<slug>", LandCoordinateCreateView.as_view(), name="add-coordinates")
]

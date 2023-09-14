from django.urls import path

from .views import (
    ProduceBookmarks,
    ProduceCreateView,
    ProduceDeleteView,
    ProduceDetailView,
    ProduceListView,
    ProduceUpdateView,
    bookmark,
    ProduceBookmarks,
)

urlpatterns = [
    path("", ProduceListView.as_view(), name="produce"),
    path("produce-detail/<slug>", ProduceDetailView.as_view(), name="produce-details"),
    path("add-produce/", ProduceCreateView.as_view(), name="add-produce"),
    path("update-produce/<slug>", ProduceUpdateView.as_view(), name="update-produce"),
    path("delete-produce/<slug>", ProduceDeleteView.as_view(), name="delete-produce"),
    path("bookmark/<slug>", bookmark, name="bookmark"),
    path("produce-bookmarks/", ProduceBookmarks.as_view(), name="produce-bookmarks")
]

from django.urls import path

from .views import (
    MyToolBookmarks,
    MyTools,
    ToolByCategory,
    ToolByTag,
    ToolCreateView,
    ToolDetailView,
    ToolListView,
    UsersTool,
    bookmark,
    ToolDeleteView,
    ToolUpdateView,
    ToolFilterView,
    add_to_cart
)

urlpatterns = [
    path("", ToolListView.as_view(), name="tools"),
    path("add-tool/", ToolCreateView.as_view(), name="add-tools"),
    path("tool-details/<slug>", ToolDetailView.as_view(), name="tool-details"),
    path("tool-delete/<slug>", ToolDeleteView.as_view(), name="tool-delete"),
    path("tool-updates/<slug>", ToolUpdateView.as_view(), name="tool-update"),
    path(
        "tool-bookmarks/<username>", MyToolBookmarks.as_view(), name="my-tool-bookmarks"
    ),
    path("bookmark/<slug>", bookmark, name="tool-bookmark"),
    path("my-tools/", MyTools.as_view(), name="my-tools"),
    path("users-tools/<username>", UsersTool.as_view(), name="users-tools"),
    path("tool-category/<slug>", ToolByCategory.as_view(), name="tool-category"),
    path("tool-tags/<slug>", ToolByTag.as_view(), name="tool-tags"),
    path("tool-filters/", ToolFilterView.as_view(), name="tool-filter"),
    path('add-cart/<int:content_type_id>/<int:object_id>/',add_to_cart,name="add-cart"),
]

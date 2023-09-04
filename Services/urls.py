from django.urls import path

from .views import (
    ServiceCreateView,
    ServiceDeleteView,
    ServiceDetailView,
    ServiceListView,
    ServiceUpdateView,
    bookmark,
    ServiceBookmarks,
    MyServices,
    UsersService,
    ServiceByCategory,
    ServiceByTag,
    ServiceFilterView
)

urlpatterns = [
    # path("/", .as_view(), name="")
    path("", ServiceListView.as_view(), name="services"),
    path("add-service/", ServiceCreateView.as_view(), name="add-services"),
    path("service-details/<slug>", ServiceDetailView.as_view(), name="service-details"),
    path("service-delete/<slug>", ServiceDeleteView.as_view(), name="service-delete"),
    path("service-updates/<slug>", ServiceUpdateView.as_view(), name="service-update"),
    path(
        "service-bookmarks/<username>", ServiceBookmarks.as_view(), name="my-service-bookmarks"
    ),
    path("bookmark/<slug>", bookmark, name="service-bookmark"),
    path("my-tools/", MyServices.as_view(), name="my-services"),
    path("users-tools/<username>", UsersService.as_view(), name="users-services"),
    path("service-category/<slug>", ServiceByCategory.as_view(), name="service-category"),
    path("service-tags/<slug>", ServiceByTag.as_view(), name="service-tags"),
    path("service-filter/", ServiceFilterView.as_view(), name="service-filter")

]

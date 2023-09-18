from django.urls import path

from .views import BidCreateView, BidDetailView, MyBidsListView,BidUpdateView,BidDeleteView

app_name = "bids"
urlpatterns = [
    path("bid-details/<slug>/", BidDetailView.as_view(), name="bid-details"),
    path("add-bid/<slug>", BidCreateView.as_view(), name="add-bids"),
    path("my-bids/", MyBidsListView.as_view(), name="my-bids"),
    path("update-bid/<slug>", BidUpdateView.as_view(), name="update-bids"),
    path("delete-bids/<slug>/", BidDeleteView.as_view(), name="delete-bids"),
]

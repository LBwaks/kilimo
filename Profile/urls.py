from django.urls import path
from .views import ProfileUpdateView,ProfileView

urlpatterns = [
    path("profile-update/<slug>", ProfileUpdateView.as_view(), name="profile-update"),
    path("profile/<slug>", ProfileView.as_view(), name="profile"),
]

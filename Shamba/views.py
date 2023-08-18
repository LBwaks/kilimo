from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Land

# Create your views here.


class LandListView(ListView):
    model = Land
    template_name = "lands/lands.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related(
            "period_lease", "owner"
        )  # .prefetch_related()
        return queryset


class LandDetailView(DetailView):
    model = Land
    template_name = "lands/land-detail.html"
    # create a folium map center 
    # add a marker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["land"] = self.get_object()
        return context

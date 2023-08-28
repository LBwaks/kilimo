from django.shortcuts import render
from .models import ServiceCategory,ServiceTag,Service,ServiceImage,BookmarkedService
from django.views.generic import ListView
# Create your views here.


class ServiceListView(ListView):
    model = Service
    template_name = "services/services.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("user","category").prefetch_related("tags")
        return queryset
    

from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Produce,ProduceCategory,ProduceTag
from .forms import ProduceForm,UpdateProduceForm
from django.contrib import messages
# Create your views here.


class ProduceListView(ListView):
    model = Produce
    template_name = "produce/produce.html"
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user','category').prefetch_related('tags')
        return queryset
    

class ProduceDetailView(DetailView):
    model = Produce
    template_name = "produce/produce-details.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["produce"] = self.get_object()
        return context
    

class ProduceCreateView(CreateView):
    model = Produce
    template_name = "produce/add-produce.html"
    form_class = ProduceForm
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        produce = form.save(commit=False)
        produce.user = self.request.user
        produce.save()
        return super().form_valid(form)

class ProduceUpdateView(UpdateView):
    model = Produce
    template_name = "produce/update-produce.html"
    form_class = UpdateProduceForm
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(request, "You dont have permission to edit this job")
            return redirect(reverse("service-details", args=[obj.slug]))

        return super().dispatch(request, *args, **kwargs)

class ProduceDeleteView(DeleteView):
    model = Produce
    template_name = "produce/delete-produce.html"
    success_url = "produce"
    success_message = "service updated"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(request, "You dont have permission to edit this job")
            return redirect(reverse("service-details", args=[obj.slug]))

        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

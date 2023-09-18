from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from .forms import BidForm,EditBidForm
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from .models import Bid
from Produce.models import Produce
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


class BidCreateView(CreateView):
    model = Bid
    form_class = BidForm
    template_name = "bids/add-bid.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        bid = form.save(commit=False)
        bid.user = self.request.user
        slug = self.kwargs["slug"]
        bid.produce =Produce.objects.get(slug=slug)
        bid.save()
        return super(BidCreateView,self).form_valid(form)
    def get_success_url(self) -> str:
        return reverse_lazy('produce')

class MyBidsListView(ListView):
    model = Bid
    template_name = "bids/my-bids.html"
    context_object_name ='bids'
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user','produce').filter(user = self.request.user)
        return  queryset
    

class BidDetailView(DetailView):
    model = Bid
    template_name = "bids/bid-details.html"
    slug_field = "uuid"
    slug_url_kwarg = "slug"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bid"] = self.get_object()
        return context
    

class BidUpdateView(UpdateView):
    model = Bid
    template_name = "bids/update-bid.html"
    form_class = EditBidForm
    success_url ="bids:my-bids"
    slug_field = "uuid"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("bids:my-bids")
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(request, "You dont have permission to edit this ")
            return redirect(reverse("bids:bid-details", args=[obj.uuid]))

        return super().dispatch(request, *args, **kwargs)



class BidDeleteView(DeleteView):
    model = Bid
    template_name = "bids/delete-bid.html"
    success_url ="bids:my-bids"
    slug_field = "uuid"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("bids:my-bids")
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(request, "You dont have permission to edit this ")
            return redirect(reverse("bids:bid-details", args=[obj.uuid]))

        return super().dispatch(request, *args, **kwargs)



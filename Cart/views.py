from django.shortcuts import render
from django.views.generic import ListView
from .models import Cart,CartItem
# Create your views here.

class CartListView(ListView):
    model = CartItem
    template_name = "cart/cart.html"
    
    def get_queryset(self):
        queryset=super().get_queryset().filter(cart__user=self.request.user)
        return queryset
    

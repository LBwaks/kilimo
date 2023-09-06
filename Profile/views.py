from django.shortcuts import get_object_or_404, render
from .forms import ProfileForm
from Profile.models import Profile
from django.views.generic import UpdateView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = "profiles/update-profile.html"
    form_class =ProfileForm
    

class ProfileView(TemplateView):
    
    template_name = "profiles/profile.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user= self.request.user
        context["profile"] = get_object_or_404(Profile.objects.select_related('user'),user=user)
        return context
    


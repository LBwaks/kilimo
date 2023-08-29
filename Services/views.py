from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import ServiceCategory,ServiceTag,Service,ServiceImage,BookmarkedService
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import ServiceForm,ServiceUpdateForm
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


class ServiceListView(ListView):
    model = Service
    template_name = "services/services.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("user","category").prefetch_related("tags")
        return queryset


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/service-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service"] = self.get_object()
        return context



class ServiceCreateView(CreateView):
    model = Service
    template_name = "services/add-services.html"
    form_class = ServiceForm
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        service = form.save(commit=False)
        service.user = self.request.user
        images = self.request.FILES.getlist("images")
        for image in images:
            ServiceImage.objects.create(service=service,image=image)
        service.save()
        return super().form_valid(form)


class ServiceUpdateView(UpdateView):
    model = Service
    template_name = "services/update-services.html"
    form_class = ServiceUpdateForm
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(request, "You dont have permission to edit this job")
            return redirect(reverse("service-details", args=[obj.slug]))

        return super().dispatch(request, *args, **kwargs)

   
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        service = form.save(commit = False)
        images = self.request.FILES.getlist("images")
        for image in images:
            ServiceImage.objects.create(service=service,image=image)
        form.save_m2m()        
        return super().form_valid(form)



class ServiceDeleteView(DeleteView):
    model = Service
    template_name = "services/services-delete.html"
    success_url ="service"
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



# bookmars 
@login_required
def bookmark(request, slug):
    service = get_object_or_404(Service, slug=slug)
    bookmarked = BookmarkedService.objects.filter(service=service, user=request.user).exists()

    if bookmarked:
        BookmarkedService.objects.filter(service=service, user=request.user).delete()
        message = "service Unbookmarked"
    else:
        BookmarkedService.objects.create(service=service, user=request.user)
        message = "service Bookmarked"
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class ServiceBookmarks(ListView):
    model = BookmarkedService
    template_name = "services/service-bookmarks.html"
    context_object_name = "bookmarks"

    def get_queryset(self):
        queryset = super().get_queryset()
        bookmarks = queryset.select_related("service", "user").filter(
            user=self.request.user
        )
        return bookmarks


class MyServices(ListView):
    model = Service
    template_name = "services/my-services.html"
    context_object_name = "services"

    def get_queryset(self):
        queryset = super().get_queryset()
        services = (
            queryset.filter(user=self.request.user)
            .order_by("-created")
            .select_related("user", "category").prefetch_related('tags')
        )

        return services


class UsersService(ListView):
    model = Service
    template_name = "services/user-services.html"
    context_object_name = "services"

    def get_queryset(self):
        self.username = self.kwargs.get("username")  # get username
        slugified_username = slugify(self.username)  # convert username to slug
        user = User.objects.filter(username=slugified_username).first()
        queryset = super().get_queryset()
        if not user:
            return Service.objects.none()
        services = (
            queryset.filter(user=user)
            .order_by("-created")
            .select_related("user", "category",).prefetch_related("tags")
        )
        return services


class ServiceByCategory(ListView):
    model = Service
    template_name = "services/service-category.html"
    context_object_name = "services"

    def get_queryset(self):
        self.category = get_object_or_404(ServiceCategory, slug=self.kwargs.get("slug"))
        queryset = super().get_queryset().select_related("user", "category",).prefetch_related("tags")
        services = queryset.filter(category=self.category)
        return services
    
class ServiceByTag(ListView):
    model = Service
    template_name = "services/service-tags.html"
    context_object_name = "services"

    def get_queryset(self):
        self.tags = get_object_or_404(ServiceTag, slug=self.kwargs.get("slug"))
        queryset = super().get_queryset().select_related("user", "category",).prefetch_related("tags")
        services = queryset.filter(tags=self.tags)
        return services


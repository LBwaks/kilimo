from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django_filters.views import FilterView

from .filters import ServiceFilter
from .forms import ServiceForm, ServiceUpdateForm
from .models import (
    BookmarkedService,
    Service,
    ServiceCategory,
    ServiceImage,
    ServiceTag,
)
from django.contrib.contenttypes.models import ContentType
# from Cart.models import Cart , CartItem

# Create your views here.


class ServiceListView(ListView):
    model = Service
    template_name = "services/services.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("user", "category").prefetch_related("tags")
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ServiceListView, self).get_context_data(**kwargs)
        context["filter"] = ServiceFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        context["popular_tags"] = ServiceTag.objects.annotate(
            num_services=Count("service")
        ).order_by("-num_services")[:5]
        context["categories"] = ServiceCategory.objects.select_related("user")
        context["tags"] = ServiceTag.objects.select_related("user", "category")

        return context


class ServiceDetailView(DetailView):
    model = Service
    template_name = "services/service-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.get_object()
        content_type = ContentType.objects.get_for_model(Service)
        tag_ids = service.tags.values_list("id", flat=True)
        print(tag_ids)
        similar_services = (
            Service.objects.select_related("user", "category")
            .prefetch_related("tags")
            .filter(Q(category=service.category) | Q(tags__in=tag_ids))
            .exclude(id=service.id)[:5]
        )
        context = {"service": service, "similar_services": similar_services,"content_type":content_type}
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
            ServiceImage.objects.create(service=service, image=image)
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
        service = form.save(commit=False)
        images = self.request.FILES.getlist("images")
        for image in images:
            ServiceImage.objects.create(service=service, image=image)
        form.save_m2m()
        return super().form_valid(form)


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = "services/services-delete.html"
    success_url = "service"
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


# bookmarks
@login_required
def bookmark(request, slug):
    service = get_object_or_404(Service, slug=slug)
    bookmarked = BookmarkedService.objects.filter(
        service=service, user=request.user
    ).exists()

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
            .select_related("user", "category")
            .prefetch_related("tags")
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
            .select_related(
                "user",
                "category",
            )
            .prefetch_related("tags")
        )
        return services


class ServiceByCategory(ListView):
    model = Service
    template_name = "services/service-category.html"
    context_object_name = "services"

    def get_queryset(self):
        self.category = get_object_or_404(ServiceCategory, slug=self.kwargs.get("slug"))
        queryset = (
            super()
            .get_queryset()
            .select_related(
                "user",
                "category",
            )
            .prefetch_related("tags")
        )
        services = queryset.filter(category=self.category)
        return services


class ServiceByTag(ListView):
    model = Service
    template_name = "services/service-tags.html"
    context_object_name = "services"

    def get_queryset(self):
        self.tags = get_object_or_404(ServiceTag, slug=self.kwargs.get("slug"))
        queryset = (
            super()
            .get_queryset()
            .select_related(
                "user",
                "category",
            )
            .prefetch_related("tags")
        )
        services = queryset.filter(tags=self.tags)
        return services


class ServiceFilterView(FilterView):
    model = Service
    template_name = "services/service-filters.html"
    filterset_class = ServiceFilter
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        service_filter = ServiceFilter(request.GET, queryset=self.get_queryset())
        paginator = Paginator(service_filter.qs, self.paginate_by)
        page_number = request.GET.get("page")
        services = paginator.get_page(page_number)
        tags = ServiceTag.objects.select_related("user", "category")
        categories = ServiceCategory.objects.select_related("user")
        return render(
            request,
            self.template_name,
            {
                "services": services,
                "tags": tags,
                "categories": categories,
                "service_filter": service_filter,
            },
        )

    def get_queryset(self):
        queryset = Service.objects.select_related("user", "category").prefetch_related(
            "tags"
        )
        service_filter = ServiceFilter(self.request.GET, queryset=queryset)

        return service_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service_filter"] = ServiceFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context

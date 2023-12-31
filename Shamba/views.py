import os
from typing import Any

from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
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
from formtools.wizard.views import SessionWizardView
from django.db.models import Count,Q
from .filters import LandFilter
from .forms import LandImagesForm  # LandCoordinatesForm,
from .forms import (
    LandCoordinatesForm,
    LandForm,
    LandInfrastructureForm,
    LandLocationForm,
    LandResourcesForm,
    LandUpdateForm,
)
from .models import (
    BookmarkedLand,
    Land,
    LandCategory,
    LandCoordiates,
    LandImages,
    LandTag,
)
from django.contrib.contenttypes.models import  ContentType
from Cart.models import Cart, CartItem
# Create your views here.


class LandListView(ListView):
    model = Land
    template_name = "lands/lands.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related(
            "period_lease", "owner", "category"
        ).prefetch_related("tags")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = LandFilter(self.request.GET, queryset=self.get_queryset())
        context['popular_tags']=LandTag.objects.annotate(num_lands=Count('land')).order_by('-num_lands')[:5]
        context["categories"] = LandCategory.objects.select_related("user")
        context["tags"] = LandTag.objects.select_related("user", "category")
        return context


class LandDetailView(DetailView):
    model = Land
    template_name = "lands/land-detail.html"
    # create a folium map center
    # add a marker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        land = self.get_object()
        content_type = ContentType.objects.get_for_model(Land)
        tags_id = land.tags.values_list('id',flat = True)
        similar_lands = Land.objects.prefetch_related('tags').select_related('owner','category','period_lease').filter(Q(category=land.category)| Q(tags__in = tags_id)).exclude(id=land.id)[:5]       
        context ={'land':land,"similar_lands":similar_lands,"content_type":content_type}
        return context


# def show_coordinates_form(wizard):
#     cleaned_data = wizard.get_cleaned_data_for_step('3') or {}
#     return cleaned_data.get("show_coordinates")


class LandWizard(SessionWizardView):
    form_list = [
        LandForm,
        LandResourcesForm,
        LandInfrastructureForm,
        LandLocationForm,
        LandImagesForm,
    ]
    template_name = "lands/add-land.html"
    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, "media/lands")
    )

    # condition_dict={'8':show_coordinates_form}
    def done(self, form_list, **kwargs):
        # file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'media/lands'))
        # for index, form_class in enumerate(form_list):
        #   print(f"Index: {index}, Form Class: {form_class.__name__}")
        # return render(self.request, 'done.html', {
        #     'form_data': [form.cleaned_data for form in form_list],
        # })
        land_data = form_list[0].cleaned_data
        land_resourse_data = form_list[1].cleaned_data
        land_infrastructure_data = form_list[2].cleaned_data
        land_location_data = form_list[3].cleaned_data
        # land_coordinates_data=form_list[8]

        land = Land.objects.create(
            owner=self.request.user,
            # form_list 1
            title=land_data["title"],
            shamba_id=land_data["shamba_id"],
            size=land_data["size"],
            charge=land_data["charge"],
            period_lease=land_data["period_lease"],
            category=land_data["category"],
            tags=land_data["tags"],
            # form_list 2
            climate=land_resourse_data["climate"],
            soil_type=land_resourse_data["soil_type"],
            water_source=land_resourse_data["water_source"],
            electricity_source=land_resourse_data["electricity_source"],
            recommended_farming=land_resourse_data["recommended_farming"],
            # form_list 3
            existing_infrastructure=land_infrastructure_data["existing_infrastructure"],
            previous_farming=land_infrastructure_data["previous_farming"],
            existing_machinery=land_infrastructure_data["existing_machinery"],
            human_labour=land_infrastructure_data["human_labour"],
            # form_list 4
            zipcode=land_location_data["zipcode"],
            county=land_location_data["county"],
            sub_county=land_location_data["sub_county"],
            location=land_location_data["location"],
            sub_location=land_location_data["sub_location"],
            village=land_location_data["village"],
            # form_list 8
            # location_coordinates=land_coordinates_data["location_coordinates"]
        )
        land_images_data = form_list[4].cleaned_data
        land_images = LandImages.objects.create(
            land=land, images=land_images_data["images"]
        )
        # land_images.land = land
        # land_images.save()
        # return HttpResponse("Form submitted")
        # Redirect to the detail page using the reverse function
        detail_url = reverse("land-details", kwargs={"slug": land.slug})
        return redirect(detail_url)


class LandCoordinateCreateView(CreateView):
    model = LandCoordiates
    template_name = "lands/add-coordinates.html"
    form_class = LandCoordinatesForm


class LandUpdateView(UpdateView):
    model = Land
    template_name = "lands/land-update.html"
    form_class = LandUpdateForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            messages.error(request, "You dont have permission to edit this job")
            return redirect(reverse("land-details", args=[obj.slug]))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        land = form.save(commit=False)
        images = self.request.FILES.getlist("images")
        for image in images:
            LandImages.objects.create(land=land, images=image)
        self.object = form.save()
        form.save_m2m()
        return super(LandUpdateView, self).form_valid(form)


class LandDeleteView(DeleteView):
    model = Land
    template_name = "lands/land-delete.html"
    success_url = "land"
    success_message = "Land updated"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            messages.error(request, "You dont have permission to Delete  this job")
            return redirect(reverse("job-details", args=[obj.slug]))
            # raise  PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


@login_required
def bookmark(request, slug):
    land = get_object_or_404(Land, slug=slug)
    bookmarked = BookmarkedLand.objects.filter(land=land, user=request.user).exists()

    if bookmarked:
        BookmarkedLand.objects.filter(land=land, user=request.user).delete()
        message = "Land Unbookmarked"
    else:
        BookmarkedLand.objects.create(land=land, user=request.user)
        message = "Land Bookmarked"
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class MyBookmarks(ListView):
    model = BookmarkedLand
    template_name = "lands/bookmarks.html"
    context_object_name = "bookmarks"

    def get_queryset(self):
        queryset = super().get_queryset()
        bookmarks = queryset.select_related("land", "user").filter(
            user=self.request.user
        )
        return bookmarks


class MyLands(ListView):
    model = Land
    template_name = "lands/my-lands.html"
    context_object_name = "lands"

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .order_by("-created")
            .select_related("owner", "category", "period_lease")
            .prefetch_related("tags")
        )
        lands = queryset.filter(owner=self.request.user)

        return lands


class UsersLand(ListView):
    model = Land
    template_name = "lands/user-lands.html"
    context_object_name = "lands"

    def get_queryset(self):
        self.username = self.kwargs.get("username")  # get username
        slugified_username = slugify(self.username)  # convert username to slug
        user = User.objects.filter(username=slugified_username).first()
        queryset = (
            super()
            .get_queryset()
            .order_by("-created")
            .select_related("owner", "category", "period_lease")
            .prefetch_related("tags")
        )
        if not user:
            return Land.objects.none()
        lands = queryset.filter(owner=user)
        return lands


class LandByCategory(ListView):
    model = Land
    template_name = "lands/land-category.html"
    context_object_name = "lands"
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(LandCategory, slug=self.kwargs.get("slug"))
        queryset = (
            super()
            .get_queryset()
            .order_by("-created")
            .select_related("owner", "category", "period_lease")
            .prefetch_related("tags")
        )
        lands = queryset.filter(category=self.category)
        return lands


class LandByTag(ListView):
    model = Land
    template_name = "lands/land-tags.html"
    context_object_name = "lands"
    paginate_by = 10

    def get_queryset(self):
        self.tag = get_object_or_404(LandTag, slug=self.kwargs.get("slug"))
        queryset = (
            super()
            .get_queryset()
            .order_by("-created")
            .select_related("owner", "category", "period_lease")
            .prefetch_related("tags")
        )
        lands = queryset.filter(tags=self.tag)
        return lands


class LandFilterView(FilterView):
    model = Land
    template_name = "lands/land-filters.html"
    filterset_class = LandFilter
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        land_filter = LandFilter(request.GET, queryset=self.get_queryset())
        paginator = Paginator(land_filter.qs, self.paginate_by)
        page_number = request.GET.get("page")
        lands = paginator.get_page(page_number)
        tags = LandTag.objects.select_related("user", "category")
        categories = LandCategory.objects.select_related("user")

        # return super().get(request, *args, **kwargs)
        return render(
            request,
            self.template_name,
            {
                "lands": lands,
                "tags": tags,
                "categories": categories,
                "land_filter": land_filter,
            },
        )

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Land.objects.select_related(
            "owner", "category", "period_lease"
        ).prefetch_related("tags")
        land_filter = LandFilter(self.request.GET, queryset=queryset)
        return land_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["land_filter"] = LandFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context

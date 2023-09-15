from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Produce,ProduceCategory,ProduceTag,ProduceBookmark
from django.contrib.auth.decorators import login_required
from .forms import ProduceForm,UpdateProduceForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.text import slugify
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

# bookmarks
@login_required
def bookmark(request, slug):
    produce = get_object_or_404(Produce, slug=slug)
    bookmarked = ProduceBookmark.objects.filter(
        produce=produce, user=request.user
    ).exists()

    if bookmarked:
        ProduceBookmark.objects.filter(produce=produce, user=request.user).delete()
        message = "produce Unbookmarked"
    else:
        ProduceBookmark.objects.create(produce=produce, user=request.user)
        message = "produce Bookmarked"
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class ProduceBookmarks(ListView):
    model = ProduceBookmark
    template_name = "produce/produce-bookmarks.html"
    context_object_name = "bookmarks"

    def get_queryset(self):
        queryset = super().get_queryset()
        bookmarks = queryset.select_related("produce", "user").filter(
            user=self.request.user
        )
        return bookmarks

class MyProduce(ListView):
    model = Produce
    template_name = "produce/my-produce.html"
    context_object_name = "produces"

    def get_queryset(self):
        queryset = super().get_queryset()
        produces = (
            queryset.filter(user=self.request.user)
            .order_by("-created")
            .select_related("user", "category")
            .prefetch_related("tags")
        )

        return produces


class UsersProduce(ListView):
    model = Produce
    template_name = "produce/user-produce.html"
    context_object_name = "produces"

    def get_queryset(self):
        self.username = self.kwargs.get("username")  # get username
        slugified_username = slugify(self.username)  # convert username to slug
        user = User.objects.filter(username=slugified_username).first()
        queryset = super().get_queryset()
        if not user:
            return Produce.objects.none()
        produces = (
            queryset.filter(user=user)
            .order_by("-created")
            .select_related(
                "user",
                "category",
            )
            .prefetch_related("tags")
        )
        return produces


class ProduceByCategory(ListView):
    model = Produce
    template_name = "produce/produce-category.html"
    context_object_name = "produces"

    def get_queryset(self):
        self.category = get_object_or_404(ProduceCategory, slug=self.kwargs.get("slug"))
        queryset = (
            super()
            .get_queryset()
            .select_related(
                "user",
                "category",
            )
            .prefetch_related("tags")
        )
        produces = queryset.filter(category=self.category)
        return produces


class ProduceByTag(ListView):
    model = Produce
    template_name = "produce/produce-tags.html"
    context_object_name = "produces"

    def get_queryset(self):
        self.tags = get_object_or_404(ProduceTag, slug=self.kwargs.get("slug"))
        queryset = (
            super()
            .get_queryset()
            .select_related(
                "user",
                "category",
            )
            .prefetch_related("tags")
        )
        produces = queryset.filter(tags=self.tags)
        return produces


class ProduceFilterView(FilterView):
    model = Produce
    template_name = "produce/produce-filters.html"
    filterset_class = ProduceFilter
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        produce_filter = ProduceFilter(request.GET, queryset=self.get_queryset())
        paginator = Paginator(produce_filter.qs, self.paginate_by)
        page_number = request.GET.get("page")
        produces = paginator.get_page(page_number)
        tags = ProduceTag.objects.select_related("user", "category")
        categories = ProduceCategory.objects.select_related("user")
        return render(
            request,
            self.template_name,
            {
                "produces": produces,
                "tags": tags,
                "categories": categories,
                "produce_filter": produce_filter,
            },
        )

    def get_queryset(self):
        queryset = Produce.objects.select_related("user", "category").prefetch_related(
            "tags"
        )
        produce_filter = ProduceFilter(self.request.GET, queryset=queryset)

        return produce_filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["produce_filter"] = ProduceFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context



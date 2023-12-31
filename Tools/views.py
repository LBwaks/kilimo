from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import BaseModelForm
from django.core.paginator import Paginator
from django_filters.views import FilterView
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

from Tools.filters import ToolFilter
from .forms import ToolForm, ToolUpdateForm
from .models import BookmarkedTool, Category, Tag, Tool, ToolImage
from django.db.models import Count,Q
from django.contrib.contenttypes.models import  ContentType
from Cart.models import Cart, CartItem
# Create your views here.


class ToolListView(ListView):
    model = Tool
    template_name = "tools/tools.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("tags").select_related("user", "category")
        return queryset
    def get_context_data(self, **kwargs):
        context = super(ToolListView,self).get_context_data(**kwargs)
        context["filter"] = ToolFilter(self.request.GET,queryset=self.get_queryset())
        context['popular_tags']=Tag.objects.annotate(num_tools=Count('tool')).order_by('-num_tools')[:5]
        context["categories"] = Category.objects.select_related("user")
        context["tags"] = Tag.objects.select_related("user", "category")
        
        return context
    

class ToolDetailView(DetailView):
    model = Tool
    template_name = "tools/tool-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_type = ContentType.objects.get_for_model(Tool)
        tool = self.get_object()
        tags_id = tool.tags.values_list('id',flat=True)
        similar_tools = Tool.objects.select_related('user','category').prefetch_related('tags').filter(Q(category=tool.category) | Q(tags__in = tags_id)).exclude(id=tool.id)[:5]
        context={'tool':tool,"similar_tools":similar_tools,'content_type':content_type}
        return context


class ToolCreateView(CreateView):
    model = Tool
    template_name = "tools/add-tools.html"
    form_class = ToolForm

    def form_valid(self, form):
        tool = form.save(commit=False)
        tool.user = self.request.user
        images = self.request.FILES.getlist('images')
        # tool_images = form.cleaned_data["images"]
        
        for image in images:
            ToolImage.objects.create(tool=tool, image=image)
            
        tool.save()
        return super(ToolCreateView,self).form_valid(form)


class ToolUpdateView(UpdateView):
    model = Tool
    template_name = "tools/tool-update.html"
    form_class = ToolUpdateForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(request, "You dont have permission to edit this job")
            return redirect(reverse("land-details", args=[obj.slug]))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        tool = form.save(commit=False)
        images = self.request.FILES.getlist("images")
        for image in images:
            ToolImage.objects.create(tool=tool, images=image)
        self.object = form.save()
        form.save_m2m()
        return super(ToolUpdateView, self).form_valid(form)


class ToolDeleteView(DeleteView):
    model = Tool
    template_name = "tools/tool-delete.html"
    success_url = "tool"
    success_message = "tool updated"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(request, "You dont have permission to Delete  this job")
            return redirect(reverse("land-details", args=[obj.slug]))
            # raise  PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


# bookmars
@login_required
def bookmark(request, slug):
    tool = get_object_or_404(Tool, slug=slug)
    bookmarked = BookmarkedTool.objects.filter(tool=tool, user=request.user).exists()

    if bookmarked:
        BookmarkedTool.objects.filter(tool=tool, user=request.user).delete()
        message = "tool Unbookmarked"
    else:
        BookmarkedTool.objects.create(tool=tool, user=request.user)
        message = "tool Bookmarked"
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class MyToolBookmarks(ListView):
    model = BookmarkedTool
    template_name = "tools/tool-bookmarks.html"
    context_object_name = "bookmarks"

    def get_queryset(self):
        queryset = super().get_queryset()
        bookmarks = queryset.select_related("tool", "user").filter(
            user=self.request.user
        )
        return bookmarks


class MyTools(ListView):
    model = Tool
    template_name = "tools/my-tools.html"
    context_object_name = "tools"

    def get_queryset(self):
        queryset = super().get_queryset()
        tools = (
            queryset.filter(user=self.request.user)
            .order_by("-created")
            .select_related("user", "category")
            .prefetch_related("tags")
        )

        return tools


class UsersTool(ListView):
    model = Tool
    template_name = "tools/user-tools.html"
    context_object_name = "tools"

    def get_queryset(self):
        self.username = self.kwargs.get("username")  # get username
        slugified_username = slugify(self.username)  # convert username to slug
        user = User.objects.filter(username=slugified_username).first()
        queryset = super().get_queryset()
        if not user:
            return Tool.objects.none()
        tools = (
            queryset.filter(user=user)
            .order_by("-created")
            .select_related(
                "user",
                "category",
            )
            .prefetch_related("tags")
        )
        return tools


class ToolByCategory(ListView):
    model = Tool
    template_name = "tools/tool-category.html"
    context_object_name = "tools"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get("slug"))
        queryset = (
            super()
            .get_queryset()
            .select_related(
                "user",
                "category",
            )
            .prefetch_related("tags")
        )
        tools = queryset.filter(category=self.category)
        return tools


class ToolByTag(ListView):
    model = Tool
    template_name = "tools/tool-tags.html"
    context_object_name = "tools"

    def get_queryset(self):
        self.tags = get_object_or_404(Tag, slug=self.kwargs.get("slug"))
        queryset = (
            super()
            .get_queryset()
            .select_related(
                "user",
                "category",
            )
            .prefetch_related("tags")
        )
        tools = queryset.filter(tags=self.tags)
        return tools


class ToolFilterView(FilterView):
    model = Tool
    template_name = "tools/tool-filters.html"
    filterset_class = ToolFilter
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        tool_filter = ToolFilter(request.GET, queryset=self.get_queryset())
        paginator = Paginator(tool_filter.qs, self.paginate_by)
        page_number = request.GET.get("page")
        tools = paginator.get_page(page_number)
        tags = Tag.objects.select_related("user", "category")
        categories = Category.objects.select_related("user")
        return render(
            request,
            self.template_name,
            {
                "tools": tools,
                "tags": tags,
                "categories": categories,
                "tool_filter": tool_filter,
            },
        )
    def get_queryset(self):
        queryset =Tool.objects.select_related('user','category').prefetch_related('tags')
        tool_filter =ToolFilter(self.request.GET,queryset=queryset)
        
        return tool_filter.qs
    def  get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tool_filter"] = ToolFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
def add_to_cart(request,content_type_id,object_id):
    content_type = get_object_or_404(ContentType,id=content_type_id)
    content_object =content_type.get_object_for_this_type(id=object_id)
    if request.user.is_authenticated:
        cart,created= Cart.objects.get_or_create(user=request.user)
        cart.add_item(content_object)
    return redirect('cart')
        
    
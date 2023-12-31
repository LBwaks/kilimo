from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext as _ 
from django_extensions.db.fields import AutoSlugField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from Shamba.choices import COUNTY,SUBCOUNTY,SUBLOCATION,LOCATION,PERIOD
from ckeditor.fields import RichTextField
from django.contrib.postgres.indexes import GinIndex


# Create your models here.

class Category(models.Model):
    """Model definition for Category."""

    # TODO: Define fields here
    title = models.CharField(max_length=50, unique=True)    
    slug = AutoSlugField(populate_from="title")
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, verbose_name=_(""),related_name="tool_category_user", on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    # objects = models.Manager()
    # publishedCategory =CategoryManager()
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'

    def __str__(self):
        """Unicode representation of Category."""
        return self.title

    # def save(self):
    #     """Save method for Category."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Category."""
        return ('')

    # TODO: Define custom methods here
    def slugify_function(self, content):
        return content.replace('_', '-').lower()

# Taggable model for tools
# class TaggedTools(TaggedItemBase):
#     content_object = models.ForeignKey('Tool', on_delete=models.CASCADE)

class Tag(models.Model):
    """Model definition for Tag."""

    # TODO: Define fields here
    name = models.CharField(max_length=50, unique=True)    
    slug = AutoSlugField(populate_from="name")
    user = models.ForeignKey(User, verbose_name=_(""),related_name="tool_tag_user", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Tag."""

        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        """Unicode representation of Tag."""
        return self.name

    # def save(self):
    #     """Save method for Tag."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Tag."""
        return ('')

    # TODO: Define custom methods here
    def slugify_function(self, content):
        return content.replace('_', '-').lower()

class Tool(models.Model):
    """Model definition for Tool."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    title =models.CharField(_("Name"), max_length=50,db_index=True)
    slug =AutoSlugField(populate_from="title")
    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name=_("Tags"))
    price = models.CharField(_("Price"), max_length=50)
    period = models.CharField(_("Period Per Price"), choices=PERIOD,max_length=50,db_index=True)
    inventory = models.IntegerField(default=1)
    county = models.CharField(_("County"), choices=COUNTY, max_length=50,db_index=True)
    sub_county = models.CharField(_("Subcounty"), choices=SUBCOUNTY, max_length=50,db_index=True)
    location = models.CharField(_("Location"), choices=LOCATION, max_length=50,db_index=True)
    sub_location = models.CharField(
        _("Sublocation"), choices=SUBLOCATION, max_length=50,db_index=True
    )
    village = models.CharField(_("Village/Estate"), max_length=50,db_index=True)
    description = RichTextField(_('Description About the tool'))
    updated = models.DateTimeField( auto_now=True, auto_now_add=False)
    created = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Tool."""

        verbose_name = 'Tool'
        verbose_name_plural = 'Tools'
        # indexes = [
        #     GinIndex(name='ToolGinIndex',fields=['title','county','sub_county','location','sub_location','village'], opclasses=[
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #         ],)
        # ]

    def __str__(self):
        """Unicode representation of Tool."""
        return self.title

    # def save(self):
    #     """Save method for Tool."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Tool."""
        return reverse('tool-details' ,kwargs={"slug":self.slug})

    # TODO: Define custom methods here
    def slugify_function(self, content):
        return content.replace('_', '-').lower()

class ToolImage(models.Model):
    """Model definition for ToolImage."""

    # TODO: Define fields here
    tool= models.ForeignKey(Tool, verbose_name=_(""), related_name='tool_images',on_delete=models.CASCADE)
    image = models.ImageField(_(""), upload_to="tools",)
    created = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)
    class Meta:
        """Meta definition for ToolImage."""
        

        verbose_name = 'Tool Image'
        verbose_name_plural = 'Tool Images'

    def __str__(self):
        """Unicode representation of ToolImage."""
        return f'{self.tool.title}-{self.id}'

    # def save(self):
    #     """Save method for ToolImage."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for ToolImage."""
        return ('')

    # TODO: Define custom methods here
class BookmarkedTool(models.Model):
    """Model definition for BookmarkedTool."""

    # TODO: Define fields here
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool = models.ForeignKey(Tool, related_name="bookmarked_tools" ,on_delete=models.CASCADE)
    bookmark_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for BookmarkedTools."""

        verbose_name = 'BookmarkedTools'
        verbose_name_plural = 'BookmarkedToolss'

    def __str__(self):
        """Unicode representation of BookmarkedTools."""
        return f"{self.user.username} saved {self.tool.title}"

    # def save(self):
    #     """Save method for BookmarkedTool."""
    #     pass

    # def get_absolute_url(self):
    #     """Return absolute url for BookmarkedTool."""
    #     return ('')

    # TODO: Define custom methods here
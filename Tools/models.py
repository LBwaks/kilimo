from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _ 
from django_extensions.db.fields import AutoSlugField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from Shamba.choices import COUNTY,SUBCOUNTY,SUBLOCATION,LOCATION,PERIOD
from ckeditor.fields import RichTextField
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

class Tool(models.Model):
    """Model definition for Tool."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    title =models.CharField(_("Name"), max_length=50)
    slug =AutoSlugField(populate_from="title")
    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.CASCADE)
    tags = models.ForeignKey(Tag, verbose_name=_("Tags"), on_delete=models.CASCADE)
    price = models.CharField(_("Price"), max_length=50)
    period = models.CharField(_("Period Per Price"), choices=PERIOD,max_length=50)
    county = models.CharField(_("County"), choices=COUNTY, max_length=50)
    sub_county = models.CharField(_("Subcounty"), choices=SUBCOUNTY, max_length=50)
    location = models.CharField(_("Location"), choices=LOCATION, max_length=50)
    sub_location = models.CharField(
        _("Sublocation"), choices=SUBLOCATION, max_length=50
    )
    village = models.CharField(_("Village/Estate"), max_length=50)
    description = RichTextField(_('Description About the tool'))
    updated = models.DateTimeField( auto_now=True, auto_now_add=False)
    created = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Tool."""

        verbose_name = 'Tool'
        verbose_name_plural = 'Tools'

    def __str__(self):
        """Unicode representation of Tool."""
        return self.title

    # def save(self):
    #     """Save method for Tool."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Tool."""
        return ('')

    # TODO: Define custom methods here

class ToolImage(models.Model):
    """Model definition for ToolImage."""

    # TODO: Define fields here
    tools= models.ForeignKey(Tool, verbose_name=_(""), on_delete=models.CASCADE)
    image = models.ImageField(_(""), upload_to="tools", height_field=None, width_field=None, max_length=None)
    created = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)
    class Meta:
        """Meta definition for ToolImage."""
        

        verbose_name = 'ToolImage'
        verbose_name_plural = 'ToolImages'

    def __str__(self):
        """Unicode representation of ToolImage."""
        pass

    # def save(self):
    #     """Save method for ToolImage."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for ToolImage."""
        return ('')

    # TODO: Define custom methods here

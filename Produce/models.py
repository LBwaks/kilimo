from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from ckeditor.fields import RichTextField
from .choices import ORGANIC,CONTROL
# Create your models here.

class ProduceCategory(models.Model):
    """Model definition for ProduceCategory."""

    # TODO: Define fields here
    title = models.CharField(max_length=50, unique=True)    
    slug = AutoSlugField(populate_from="title")
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, verbose_name=_(""),related_name="produce_category_user", on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    # objects = models.Manager()
    # publishedCategory =CategoryManager()
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for ProduceCategory."""

        verbose_name = 'Produce Category'
        verbose_name_plural = 'Produce Categoryies'

    def __str__(self):
        """Unicode representation of ProduceCategory."""
        return self.title

    # def save(self):
    #     """Save method for ProduceCategory."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Produce Category."""
        return ('')

    # TODO: Define custom methods here

class ProduceTag(models.Model):
    """Model definition for Tag."""

    # TODO: Define fields here
    name = models.CharField(max_length=50, unique=True)    
    slug = AutoSlugField(populate_from="name")
    user = models.ForeignKey(User, verbose_name=_(""),related_name="produce_tag_user", on_delete=models.CASCADE)
    category = models.ForeignKey(ProduceCategory, verbose_name=_("Category"), on_delete=models.CASCADE)
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


class Produce(models.Model):
    """Model definition for Produce."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    title =models.CharField(_("Name"), max_length=50,db_index=True)
    slug =AutoSlugField(populate_from="title")
    category = models.ForeignKey(ProduceCategory, verbose_name=_("Category"), on_delete=models.CASCADE)
    tags = models.ManyToManyField(ProduceTag, verbose_name=_("Tags"))
    growth_way =models.CharField(_("Way of Growth"),choices=ORGANIC, max_length=50)
    organic_description = RichTextField(_('Description way of growth'))
    control_growth =models.CharField(_("Control growth"),choices=CONTROL, max_length=50)
    growth_period = models.CharField(_("Period Of Growth"), max_length=50)
    growth_fertilizer = models.CharField(_("Types of fertilizer"), max_length=50)
    growth_pestcides = models.CharField(_("Pesticides"), max_length=50)
    control_description = RichTextField(_('Description way of control'))

    
    # period = models.CharField(_("Period Per Price"), choices=PERIOD,max_length=50,db_index=True)
    # inventory = models.IntegerField(default=1)
    # county = models.CharField(_("County"), choices=COUNTY, max_length=50,db_index=True)
    # sub_county = models.CharField(_("Subcounty"), choices=SUBCOUNTY, max_length=50,db_index=True)
    # location = models.CharField(_("Location"), choices=LOCATION, max_length=50,db_index=True)
    
    # village = models.CharField(_("Village/Estate"), max_length=50,db_index=True)
    
    updated = models.DateTimeField( auto_now=True, auto_now_add=False)
    created = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Produce."""

        verbose_name = 'Produce'
        verbose_name_plural = 'Produces'

    def __str__(self):
        """Unicode representation of Produce."""
        return self.title

    # def save(self):
    #     """Save method for Produce."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Produce."""
        return reverse('produce-details',kwargs={"slug":self.slug})

    # TODO: Define custom methods here

# USE db_index=True
#  indexes = [
            # GinIndex(name='ProduceGinIndex',fields=['title','keywords','shortDescription','details'],,opclasses=['gin_trgm_ops'])
        # ]
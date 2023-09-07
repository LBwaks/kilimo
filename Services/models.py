from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext as _ 
from django_extensions.db.fields import AutoSlugField
# from autoslug import AutoSlugField
from Shamba.choices import COUNTY,SUBCOUNTY,SUBLOCATION,LOCATION,PERIOD
from ckeditor.fields import RichTextField
import uuid
from django.contrib.postgres.indexes import GinIndex

# Create your models here.
def my_slugify_function(content):
    return content.replace('_', '-').lower()

class ServiceCategory(models.Model):
    """Model definition for ServiceCategory."""

    # TODO: Define fields here
    title = models.CharField(max_length=50, unique=True)    
    slug =AutoSlugField(populate_from='title', slugify_function=my_slugify_function)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, verbose_name=_(""),related_name="service_category_user", on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    # objects = models.Manager()
    # publishedCategory =CategoryManager()
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for ServiceCategory."""

        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categorys'

    def __str__(self):
        """Unicode representation of ServiceCategory."""
        return self.title

    # def save(self):
    #     """Save method for ServiceCategory."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for ServiceCategory."""
        return ('')

    # TODO: Define custom methods here
    def slugify_function(self, content):
        return content.replace('_', '-').lower()


class ServiceTag(models.Model):
    """Model definition for ServiceTag."""

    # TODO: Define fields here
    name = models.CharField(max_length=50, unique=True)    
    slug =AutoSlugField(populate_from="name", slugify_function=my_slugify_function)
    user = models.ForeignKey(User, verbose_name=_(""),related_name="service_tag_user", on_delete=models.CASCADE)
    category = models.ForeignKey(ServiceCategory, related_name="service_category", verbose_name=_("Category"), on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    # is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for ServiceTag."""

        verbose_name = 'Service Tag'
        verbose_name_plural = 'Service Tags'

    def __str__(self):
        """Unicode representation of Service Tag."""
        return self.name

    # def save(self):
    #     """Save method for ServiceTag."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for ServiceTag."""
        return ('')

    # TODO: Define custom methods here


class Service(models.Model):
    """Model definition for Service."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    title =models.CharField(_("Name"), max_length=50,db_index=True)
    slug =models.UUIDField(default=uuid.uuid4, editable=False)
    category = models.ForeignKey(ServiceCategory, verbose_name=_("Category"), on_delete=models.CASCADE)
    tags = models.ManyToManyField(ServiceTag, verbose_name=_("Tags"))
    price = models.CharField(_("Price"), max_length=50)
    period = models.CharField(_("Period Per Price"), choices=PERIOD,max_length=50)
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
        """Meta definition for Service."""

        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        # indexes = [
        #     GinIndex(name='ServicesGinIndex',fields=['title','county','sub_county','location','sub_location','village'], opclasses=[
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #         ],)
        # ]

    def __str__(self):
        """Unicode representation of Service."""
        return self.title

    # def save(self):
    #     """Save method for Service."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Service."""
        return reverse('service-details',kwargs={"slug":self.slug})

    # TODO: Define custom methods here
    
    
class ServiceImage(models.Model):
    """Model definition for ServiceImage."""

    # TODO: Define fields here
    service= models.ForeignKey(Service, verbose_name=_(""), on_delete=models.CASCADE)
    image = models.ImageField(_(""), upload_to="services", height_field=None, width_field=None, max_length=None)
    created = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)
    
    class Meta:
        """Meta definition for ServiceImage."""

        verbose_name = 'Service Image'
        verbose_name_plural = 'Service Images'

    def __str__(self):
        """Unicode representation of ServiceImage."""
        pass

    # def save(self):
    #     """Save method for ServiceImage."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for ServiceImage."""
        return ('')

    # TODO: Define custom methods here

class BookmarkedService(models.Model):
    """Model definition for BookmarkedService."""

    # TODO: Define fields here
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name="bookmarked_services" ,on_delete=models.CASCADE)
    bookmark_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for BookmarkedService."""

        verbose_name = 'BookmarkedService'
        verbose_name_plural = 'BookmarkedServices'

    def __str__(self):
        """Unicode representation of BookmarkedService."""
        return f"{self.user.username} saved {self.service.title}"

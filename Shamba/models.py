import hashlib
import random
import uuid
import time
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django_extensions.db.fields import AutoSlugField
from .choices import COUNTY, LOCATION, SUBCOUNTY, SUBLOCATION,UNITS
from django.contrib.postgres.indexes import GinIndex


# Create your models here.
class LandCategory(models.Model):
    """Model definition for LandCategory."""

    # TODO: Define fields here
    user = models.ForeignKey(
        User,
        related_name="user_land_category",
        on_delete=models.CASCADE,
    )
    type = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from="type")
    description = models.TextField(max_length=250)
    is_published = models.BooleanField(default=True)
    # objects = models.Manager()
    # publishedCategory =CategoryManager()
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for LandCategory."""

        verbose_name = 'LandCategory'
        verbose_name_plural = 'LandCategorys'

    def __str__(self):
        """Unicode representation of LandCategory."""
        return self.type

    # def save(self):
    #     """Save method for LandCategory."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for LandCategory."""
        return ('')

    # TODO: Define custom methods here
    def slugify_function(self, content):
        return content.replace('_', '-').lower()
class LandTag(models.Model):
    """Model definition for LandTag."""

    # TODO: Define fields here
    name = models.CharField(max_length=50, unique=True)    
    slug =AutoSlugField(populate_from="name")
    user = models.ForeignKey(User, verbose_name=_(""),related_name="land_tag_user", on_delete=models.CASCADE)
    category = models.ForeignKey(LandCategory, related_name="land_tag_category", verbose_name=_("Category"), on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    # is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        """Meta definition for LandTag."""

        verbose_name = 'LandTag'
        verbose_name_plural = 'LandTags'

    def __str__(self):
        """Unicode representation of LandTag."""
        return self.name
        

class LeasePeriod(models.Model):
    """Model definition for LeasePeriod."""

    # TODO: Define fields here
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
    period = models.CharField(_("Period Of Lease"), max_length=50)
    other_period = models.CharField(_("Other"), max_length=50, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for LeasePeriod."""

        verbose_name = "LeasePeriod"
        verbose_name_plural = "LeasePeriods"

    def __str__(self):
        """Unicode representation of LeasePeriod."""
        return self.period

    # def save(self):
    #     """Save method for LeasePeriod."""
    #     pass

    # def get_absolute_url(self):
    #     """Return absolute url for LeasePeriod."""
    #     return ('')

    # TODO: Define custom methods here


class Land(models.Model):

    """Model definition for Lands."""

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=50,db_index=True)
    land_id = models.CharField(_("Land Id"), unique=True, max_length=12,db_index=True)
    type = models.ForeignKey(LandCategory, verbose_name=_("Category"), related_name="land_category",on_delete=models.CASCADE)
    tags = models.ManyToManyField(LandTag, verbose_name=_("Tags"))
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
    shamba_id = models.CharField(_("Proof Of Ownership"), max_length=50)
    zipcode = models.CharField(_("Zipcode"), max_length=50)
    county = models.CharField(_("County"), choices=COUNTY, max_length=50,db_index=True)
    sub_county = models.CharField(_("Subcounty"), choices=SUBCOUNTY, max_length=50,db_index=True)
    location = models.CharField(_("Location"), choices=LOCATION, max_length=50,db_index=True)
    sub_location = models.CharField(
        _("Sublocation"), choices=SUBLOCATION, max_length=50,db_index=True
    )
    village = models.CharField(_("Village/Estate"), max_length=50,db_index=True)
     
    size = models.FloatField(_("Land Size"))
    size_units = models.CharField(_("Size Unit"),choices=UNITS, max_length=50)
    soil_type = RichTextField(_("Soil type"))
    climate = RichTextField(_("Describe Region Climate"))
    previous_farming = RichTextField(_("Previous Farming Activity"))
    water_source = RichTextField(_("Sourcse of Water"))
    electricity_source = RichTextField(_("Source of Electricity"))
    period_lease = models.ForeignKey(
        LeasePeriod,
        verbose_name=_("Lease Period"),
        related_name="lease_period",
        on_delete=models.CASCADE,
    )
    charge = models.IntegerField(_("Lease Charges"))
    existing_infrastructure = RichTextField(_("Existing Infrastructure"))
    existing_machinery = RichTextField(_("Existing Machinery"))
    human_labour = RichTextField(_("Human Labour"))
    recommended_farming = RichTextField(_("Recommended Farming"))
    updated = models.DateTimeField(
        auto_now=True,
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    # TODO: Define fields here

    class Meta:
        """Meta definition for Land."""

        verbose_name = "Land"
        verbose_name_plural = "Lands"
        # indexes = [
        #     GinIndex(name='LandGinIndex',fields=['title','county','sub_county','location','sub_location','village'], opclasses=[
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #             'gin_trgm_ops',
        #         ],)
        # ]

    def __str__(self):
        """Unicode representation of Land."""
        return self.land_id

    def save(self, *args, **kwargs):
        """Save method for Land."""
        if not self.land_id:
            self.land_id = self.generate_land_id()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Return absolute url for Land."""
        return reverse("land-details", kwargs={"slug": self.slug})

    # TODO: Define custom methods here
    def generate_land_id(self):
        timestamp = int(time.time() * 1000)
        random_num = random.randint(10000000, 99999999)
        unique_id = f"{timestamp}{random_num}"
        hashed_id = hashlib.sha256(unique_id.encode()).hexdigest()[:10]
        return hashed_id
        return hashed_id


class LandImages(models.Model):
    """Model definition for LandImages."""

    # TODO: Define fields here
    land = models.ForeignKey(
        Land, verbose_name=_(""), related_name="land_images", on_delete=models.CASCADE
    )
    images = models.ImageField(
        _("Land Images"),
        upload_to="lands",
        # height_field=None,
        # width_field=None,
        # max_length=None,
        null=True,
        blank=True
    )
    updated = models.DateTimeField(
        auto_now=True,
    )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for LandImages."""

        verbose_name = "LandImages"
        verbose_name_plural = "LandImagess"

    def __str__(self):
        """Unicode representation of LandImages."""
        pass

    # def save(self):
    #     """Save method for LandImages."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for LandImages."""
        return ""

    # TODO: Define custom methods here

class BookmarkedLand(models.Model):
    """Model definition for BookmarkedLand."""

    # TODO: Define fields here
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    land = models.ForeignKey(Land, related_name="bookmarked_lands" ,on_delete=models.CASCADE)
    bookmark_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for BookmarkedLand."""

        verbose_name = 'BookmarkedLand'
        verbose_name_plural = 'BookmarkedLands'

    def __str__(self):
        """Unicode representation of BookmarkedLand."""
        return f"{self.user.username} saved {self.land.land_id}"

    # def save(self):
    #     """Save method for BookmarkedLand."""
    #     pass

    # def get_absolute_url(self):
    #     """Return absolute url for BookmarkedLand."""
    #     return ('')

    # TODO: Define custom methods here


class LandCoordiates(models.Model):
    """Model definition for LandCoordiates."""

    # TODO: Define fields here
    land = models.ForeignKey(Land, verbose_name=_(""), on_delete=models.CASCADE)
    coordinates = models.PointField(_("Coordinates"))
    updated =models.DateTimeField( auto_now=True,)
    created = models.DateTimeField( auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for LandCoordiates."""

        verbose_name = 'LandCoordiates'
        verbose_name_plural = 'LandCoordiatess'

    def __str__(self):
        """Unicode representation of LandCoordiates."""
        pass

    def save(self):
        """Save method for LandCoordiates."""
        pass

    def get_absolute_url(self):
        """Return absolute url for LandCoordiates."""
        return ('')

    # TODO: Define custom methods here

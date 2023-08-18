import hashlib
import random
import uuid
from datetime import time

# from .choices import PERIOD
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

# Create your models here.


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
    land_id = models.CharField(_("Land Id"), unique=True, max_length=12)
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
    shamba_id = models.CharField(_("Proof Of Ownership"), max_length=50)
    location = models.PointField()
    size = models.FloatField(_("Land Size"))
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
    recommended_farming = RichTextField(_("Recommended Farming"))
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    # TODO: Define fields here

    class Meta:
        """Meta definition for Land."""

        verbose_name = "Land"
        verbose_name_plural = "Lands"

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
        random_num = random.randint((10000000, 99999999))
        unique_id = f"{timestamp}{random_num}"
        hashed_id = hashlib.sha256(unique_id.encode()).hexdigest()[:10]
        return hashed_id
        return hashed_id

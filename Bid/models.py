from django.db import models
from django.contrib.auth.models import User 
from django_extensions.db.fields import AutoSlugField
from ckeditor.fields import RichTextField
from django.utils.translation import gettext as _
# Create your models here.
class Bid(models.Model):
    """Model definition for Bid."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Bid."""

        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'

    def __str__(self):
        """Unicode representation of Bid."""
        pass

    def save(self):
        """Save method for Bid."""
        pass

    def get_absolute_url(self):
        """Return absolute url for Bid."""
        return ('')

    # TODO: Define custom methods here

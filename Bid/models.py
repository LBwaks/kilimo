from django.db import models
from django.contrib.auth.models import User 
from django_extensions.db.fields import AutoSlugField
import uuid
from ckeditor.fields import RichTextField
from django.utils.translation import gettext as _
from Produce.models import Produce
# Create your models here.
class Bid(models.Model):
    """Model definition for Bid."""

    # TODO: Define fields here
    uuid =models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user =models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    produce = models.ForeignKey(Produce, verbose_name=_(""), on_delete=models.CASCADE)
    charge =models.IntegerField(_("Charge"))
    reasons =RichTextField(_("Reasons For you charge"))
    services =RichTextField(_("Other secondary Services "))
    status = models.CharField(_(""),default="PENDING", max_length=50)
    approved_cancelled_time =models.DateTimeField(_(""),blank=True, null=True)
    created = models.DateTimeField( auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Bid."""

        verbose_name = 'Bid'
        verbose_name_plural = 'Bids'

    def __str__(self):
        """Unicode representation of Bid."""
        return f"Produce {self.produce.title}, has a bid of {self.charge}"

    # def save(self):
    #     """Save method for Bid."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Bid."""
        return ('')

    # TODO: Define custom methods here

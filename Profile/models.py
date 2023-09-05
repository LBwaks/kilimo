from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from Shamba.choices import COUNTY,SUBCOUNTY,LOCATION,SUBLOCATION
from .choices import INTEREST
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from PIL import Image
# Create your models here.


ext_validators =FileExtensionValidator(['jpg','png','jpeg',''])
class Profile(models.Model):
    """Model definition for Profile."""
 
    # TODO: Define fields here
    user = models.OneToOneField(User, verbose_name=_(""), on_delete=models.CASCADE)
    firstname = models.CharField(_("Firstname"), max_length=50)
    lastname =models.CharField(_("Lastname"), max_length=50)
    slug = models.UUIDField(default=uuid.uuid4,editable=False)
    email = models.EmailField(_("Email"), max_length=254,unique=True)
    tell =PhoneNumberField(_("Phone Number"),unique=True,)
    county =models.CharField(_("County"),choices=COUNTY, max_length=50)
    sub_county = models.CharField(_("Sub County"), choices=SUBCOUNTY, max_length=50)
    location = models.CharField(_("Location"),choices=LOCATION, max_length=50)
    sub_location=models.CharField(_("Sub Location"), choices=SUBLOCATION, max_length=50)
    village = models.CharField(_("Village/Estates"), max_length=50)
    bio = RichTextField(_('Bio'),null=True, blank=True)
    interest = models.CharField(_("Interest"),choices=INTEREST, max_length=50)
    other = RichTextField(_('Explain Interest'),null=True, blank=True)
    avatar = models.ImageField(_("Profile"), upload_to='profiles',null=True, blank=True,default='profiles/profile.jpg', validators=[ext_validators])
    status = models.CharField(_("Status"),default='Active', max_length=50)
    is_suspended=models.BooleanField(_("Suspended") ,default=False)
    twitter = models.URLField(_("Twitter"), max_length=200,null=True, blank=True)
    website =models.URLField(_("Website"), max_length=200,null=True, blank=True)
    facebook = models.URLField(_("Facebook"), max_length=200,null=True, blank=True)
    created =models.DateTimeField( auto_now=False, auto_now_add=True)
    
 
    class Meta:
        """Meta definition for Profile."""
 
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
 
    def __str__(self):
        """Unicode representation of Profile."""
        return f"{str(self.firstname)} {str(self.lastname)}"
 
    def save(self,*args, **kwargs):
    #     """Save method for Profile."""
    
    # save the profile first
        super().save(*args, **kwargs)

    # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
        # create a thumbnail
            img.thumbnail(output_size)
        
        # overwrite the large image
            img.save(self.avatar.path)
 
    def get_absolute_url(self):
        """Return absolute url for Profile."""
        return ('')
 
    # TODO: Define custom methods here
 
from ckeditor.widgets import CKEditorWidget
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import Profile


class ProfileForm(forms.ModelForm):
    """Form definition for Profile."""
    other = forms.CharField(label='Please Explain',widget=CKEditorWidget(attrs={'class':'form-control other'}))
    bio = forms.CharField(label="Bio",widget=CKEditorWidget(attrs={'class':'form-control bio'}))
    tell = PhoneNumberField(region="KE",widget=PhoneNumberPrefixWidget(country_choices=[('KE','Kenya')]))
    class Meta:
        """Meta definition for Profileform."""

        model = Profile
        fields = (
            "firstname",
            "lastname",
            "email",
            "tell",
            "county",
            "sub_county",
            "location",
            "sub_location",
            "village",
            "bio",
            "interest",
            "other",
            "avatar",
            "twitter",
            "facebook",
            "website",
        )
        widgets = {
            "firstname":forms.TextInput(attrs={'class':'form-control fname',"required":True}),
            "lastname":forms.TextInput(attrs={'class':'form-control lname',"required":True}),
            "email":forms.EmailInput(attrs={'class':'form-control email',"required":True}),
            
            "county": forms.Select(attrs={'class': 'control-select county', 'required': True}),
            "sub_county": forms.Select(attrs={'class': 'control-select sub_county', 'required': True}),
            "location": forms.Select(attrs={'class': 'control-select location', 'required': True}),
            "sub_location": forms.TextInput(attrs={'class': 'control-form sub_location', 'required': True}),
            "village":forms.TextInput(attrs={'class':'form-control village',"required":True}),
            
            "interest":forms.Select(attrs={'class':'control-select interest','required':True}),
        
            "avatar":forms.ClearableFileInput(attrs={'class':'form-control','accept':'png,jpg,jpeg'}),
            "twitter":forms.URLInput(attrs={'class':'form-control twitter'}),
            "facebook":forms.URLInput(attrs={'class':'form-control facebook'}),
            "website":forms.URLInput(attrs={'class':'form-control website'}),
        }

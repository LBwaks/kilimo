from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Service, ServiceTag


class ServiceForm(forms.ModelForm):
    """Form definition for Service."""

    # images = forms.FileField(
    #     label="Image",
    #     widget=forms.ClearableFileInput(
    #         attrs={"required": True, "class": "form-control image"}
    #     ),
    # )
    tags = forms.ModelMultipleChoiceField(
        label="Tags",
        widget=forms.SelectMultiple(
            attrs={
                "required": True,
                "class": "form-control tags form-select",
                "id": "service_tags",
            }
        ),
        queryset=ServiceTag.objects.all(),
    )
    description = forms.CharField(
        label="Description",
        widget=CKEditorWidget(
            attrs={"required": True, "class": "description form-control"}
        ),
    )

    class Meta:
        """Meta definition for Serviceform."""

        model = Service
        labels ={
            "title":'Title',
            "category":'Category',            
            "price":'Price',
            "period":'Period',
            "county":'County',            
            "sub_county":'Sub County',
            "location":'Location',
            "sub_location":"Sub Location",
            "village":'Village',
            
        }
        fields = (
            "title",
            "category",
            "tags",
            "price",
            "period",
            "county",
            "sub_county",
            "location",
            "sub_location",
            "village",
            "description",
        )
        widget ={
            "title": forms.TextInput(attrs={'class': 'control-form title', 'required': True}),
            "category": forms.Select(attrs={'class': 'control-select category', 'required': True}),
            "price":forms.TextInput(attrs={'class':"form-control price",'required':True}),
            "period": forms.Select(attrs={'class': 'control-select period', 'required': True}),
            "county": forms.Select(attrs={'class': 'control-select county', 'required': True}),
            "sub_county": forms.Select(attrs={'class': 'control-select sub_county', 'required': True}),
            "location": forms.Select(attrs={'class': 'control-select location', 'required': True}),
            "sub_location": forms.TextInput(attrs={'class': 'control-form sub_location', 'required': True}),
            "village": forms.TextInput(attrs={'class': 'control-form village', 'required': True}),
        }


class ServiceUpdateForm(forms.ModelForm):
    """Form definition for Service."""

    images = forms.FileField(
        label="Image",
        widget=forms.ClearableFileInput(
            attrs={"required": True, "class": "form-control image"}
        ),
    )
    tags = forms.ModelMultipleChoiceField(
        label="Tags",
        widget=forms.SelectMultiple(
            attrs={
                "required": True,
                "class": "form-control tags form-select",
                "id": "service_tags",
            }
        ),
        queryset=ServiceTag.objects.all(),
    )
    description = forms.CharField(
        label="Description",
        widget=CKEditorWidget(
            attrs={"required": True, "class": "description form-control"}
        ),
    )

    class Meta:
        """Meta definition for Serviceform."""

        model = Service
        labels ={
            "title":'Title',
            "category":'Category',            
            "price":'Price',
            "period":'Period',
            "county":'County',            
            "sub_county":'Sub County',
            "location":'Location',
            "sub_location":"Sub Location",
            "village":'Village',
            
        }
        fields = (
            "title",
            "category",
            "tags",
            "price",
            "period",
            "county",
            "sub_county",
            "location",
            "sub_location",
            "village",
            "description",
        )
        widget ={
            "title": forms.TextInput(attrs={'class': 'control-form title', 'required': True}),
            "category": forms.Select(attrs={'class': 'control-select category', 'required': True}),
            "price":forms.TextInput(attrs={'class':"form-control price",'required':True}),
            "period": forms.Select(attrs={'class': 'control-select period', 'required': True}),
            "county": forms.Select(attrs={'class': 'control-select county', 'required': True}),
            "sub_county": forms.Select(attrs={'class': 'control-select sub_county', 'required': True}),
            "location": forms.Select(attrs={'class': 'control-select location', 'required': True}),
            "sub_location": forms.TextInput(attrs={'class': 'control-form sub_location', 'required': True}),
            "village": forms.TextInput(attrs={'class': 'control-form village', 'required': True}),
        }

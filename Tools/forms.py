from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Category, Tag, Tool, ToolImage

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
    
    
class ToolForm(forms.ModelForm):
    """Form definition for Tool."""

    tags = forms.ModelMultipleChoiceField(
        label="Tags",
        widget=forms.SelectMultiple(
            attrs={
                "required": True,
                "class": "form-control tags form-select",
                "id": "tools_tag",
            }
        ),
        queryset=Tag.objects.all()
    )
    description = forms.CharField(
        label="Description",
        widget=CKEditorWidget(
            attrs={"required": True, "class": "form-control description"}
        ),
    )
    images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={
        'required': False,
        'class': 'form-control images',
        # 'multiple': True
    }))
    # images=MultipleFileField()

    class Meta:
        """Meta definition for Toolform."""

        model = Tool
        labels = {
            "title":'Title',
            "category":'Category',           
            "price":'Price',
            "period":'Period',
            "county":'County',
            "sub_county":'Sub County',
            "location":'Location',
            "village":'Village',
            'inventory':'Available Units'
            
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
            'inventory',
        )
        widget ={
            "title": forms.TextInput(attrs={'class': 'control-form title', 'required': True}),
            "category": forms.Select(attrs={'class': 'control-select category', 'required': True}),
            "price":forms.TextInput(attrs={'class':"form-control price",'required':True}),
            "period": forms.Select(attrs={'class': 'control-select period', 'required': True}),
            "inventory":forms.TextInput(attrs={'class':"form-control inventory",'required':True}),
            "county": forms.Select(attrs={'class': 'control-select county', 'required': True}),
            "sub_county": forms.Select(attrs={'class': 'control-select sub_county', 'required': True}),
            "location": forms.Select(attrs={'class': 'control-select location', 'required': True}),
            "location": forms.TextInput(attrs={'class': 'control-form location', 'required': True}),
            "village": forms.TextInput(attrs={'class': 'control-form village', 'required': True}),
        }


class ToolUpdateForm(forms.ModelForm):
    """Form definition for Tool."""

    tags = forms.ModelMultipleChoiceField(
        label="Tags",
        widget=forms.SelectMultiple(
            attrs={
                "required": True,
                "class": "form-control tags form-select",
                "id": "tools_tag",
            }
        ),
        queryset=Tag.objects.all()
    )
    description = forms.CharField(
        label="Description",
        widget=CKEditorWidget(
            attrs={"required": True, "class": "form-control description"}
        ),
    )
    # images = forms.ImageField(
    #     # required=True,
    #     widget=forms.ClearableFileInput(
    #         attrs={ "required": True, "class": "form-control image",}
    #     ),
    # )

    class Meta:
        """Meta definition for Toolform."""

        model = Tool
        labels = {
            "title":'Title',
            "category":'Category',           
            "price":'Price',
            "period":'Period',
            "county":'County',
            "sub_county":'Sub County',
            "location":'Location',
            "village":'Village',
             'inventory':'Available Units'
            
        }
        fields = (
            "title",
            "category",
            "tags",
            "price",
            "period",
            'inventory',
            "county",
            "sub_county",
            "location",
            "village",
            "description",
        )
        widget ={
            "title": forms.TextInput(attrs={'class': 'control-form title', 'required': True}),
            "category": forms.Select(attrs={'class': 'control-select category', 'required': True}),
            "price":forms.TextInput(attrs={'class':"form-control price",'required':True}),
            "period": forms.Select(attrs={'class': 'control-select period', 'required': True}),
            "county": forms.Select(attrs={'class': 'control-select county', 'required': True}),
            "inventory":forms.TextInput(attrs={'class':"form-control inventory",'required':True}),
            "sub_county": forms.Select(attrs={'class': 'control-select sub_county', 'required': True}),
            "location": forms.Select(attrs={'class': 'control-select location', 'required': True}),
            "location": forms.TextInput(attrs={'class': 'control-form location', 'required': True}),
            "village": forms.TextInput(attrs={'class': 'control-form village', 'required': True}),
        }

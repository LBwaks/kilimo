from django import forms

from .models import Produce, ProduceTag
from ckeditor.widgets import  CKEditorWidget

class ProduceForm(forms.ModelForm):
    """Form definition for Produce."""
    tags = forms.ModelMultipleChoiceField(label='Tags',widget=forms.SelectMultiple(attrs={"class":"form-select tags","required":True,"id":"tags"}),queryset=ProduceTag.objects.all())
    organic_description = forms.CharField(label="Describe how organic",widget = CKEditorWidget(attrs={"class":"organic_description form-control","required":True})) 
    control_description =  forms.CharField(label="Describe how organic",widget = CKEditorWidget(attrs={"class":"organic_description form-control","required":True})) 

    class Meta:
        """Meta definition for Produceform."""

        model = Produce
        labels ={
            "title":"Title",
            "category":"Category",
            "tags":'Tags',
            "growth_way":'Way of Growth',
            # "organic_description":"Describe how",
            "control_growth":"Control Growth",
            "growth_period":'Period ',
            "growth_fertilizer":"Type of growth",
            "growth_pestcides":"Pestcidees",
            "control_description":'Describe control',
        }
        fields = (
            "title",
            "category",
            "tags",
            "growth_way",
            "organic_description",
            "control_growth",
            "growth_period",
            "growth_fertilizer",
            "growth_pestcides",
            "control_description",
        )
        widgets ={
            "title":forms.TextInput(attrs={"class":"form-control title","required":True}),
            "category":forms.Select(attrs={"class":"form-select category","required":True}),
            # "tags",
            "growth_way":forms.Select(attrs={"class":"form-select","required":True}),
            
            "control_growth":forms.Select(attrs={"class":"form-select",'required':True}),
            "growth_period":forms.TextInput(attrs={"class":"form-control period","required":True}),
            "growth_fertilizer":forms.TextInput(attrs={"class":"form-control fertilizer","required":True}),
            "growth_pestcides":forms.TextInput(attrs={"class":"form-control pesticides","required":True}),
            # "control_description",
        }

class UpdateProduceForm(forms.ModelForm):
    """Form definition for Produce."""
    tags = forms.ModelMultipleChoiceField(label='Tags',widget=forms.SelectMultiple(attrs={"class":"form-select tags","required":True,"id":"tags"}),queryset=ProduceTag.objects.all())
    organic_description = forms.CharField(label="Describe how organic",widget = CKEditorWidget(attrs={"class":"organic_description form-control","required":True})) 
    control_description =  forms.CharField(label="Describe how organic",widget = CKEditorWidget(attrs={"class":"organic_description form-control","required":True})) 

    class Meta:
        """Meta definition for Produceform."""

        model = Produce
        labels ={
            "title":"Title",
            "category":"Category",
            "tags":'Tags',
            "growth_way":'Way of Growth',
            # "organic_description":"Describe how",
            "control_growth":"Control Growth",
            "growth_period":'Period ',
            "growth_fertilizer":"Type of growth",
            "growth_pestcides":"Pestcidees",
            "control_description":'Describe control',
        }
        fields = (
            "title",
            "category",
            "tags",
            "growth_way",
            "organic_description",
            "control_growth",
            "growth_period",
            "growth_fertilizer",
            "growth_pestcides",
            "control_description",
        )
        widgets ={
            "title":forms.TextInput(attrs={"class":"form-control title","required":True}),
            "category":forms.Select(attrs={"class":"form-select category","required":True}),
            # "tags",
            "growth_way":forms.Select(attrs={"class":"form-select","required":True}),
            
            "control_growth":forms.Select(attrs={"class":"form-select",'required':True}),
            "growth_period":forms.TextInput(attrs={"class":"form-control period","required":True}),
            "growth_fertilizer":forms.TextInput(attrs={"class":"form-control fertilizer","required":True}),
            "growth_pestcides":forms.TextInput(attrs={"class":"form-control pesticides","required":True}),
            # "control_description",
        }

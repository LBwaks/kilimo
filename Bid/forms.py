from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Bid


class EditBidForm(forms.ModelForm):
    """Form definition for Bid."""

    class Meta:
        """Meta definition for Bidform."""

        model = Bid
        fields = ("charge", "reasons", "services")
        labels = {
            "charge": "Charge",
            "reasons": "Reasons For That Price",
            "services": "Any secondary services",
        }
        widgets ={
            "charge":forms.NumberInput(attrs={"class":"form-control charge","required":True}),
            "reasons":CKEditorWidget(attrs={"class":"form-control reasons","required":True}),
            "services":CKEditorWidget(attrs={"class":"form-control"})
        }
from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Bid


class BidForm(forms.ModelForm):
    """Form definition for Bid."""

    class Meta:
        """Meta definition for Bidform."""

        model = Bid
        fields = ("charge", "reasons", "services")
        labels = {
            "charge": "Charge",
            "reasons": "Reasons For That Price",
            "services": "Any secondary services",
        }
        widgets ={
            "charge":forms.NumberInput(attrs={"class":"form-control charge","required":True}),
            "reasons":CKEditorWidget(attrs={"class":"form-control reasons","required":True}),
            "services":CKEditorWidget(attrs={"class":"form-control"})
        }

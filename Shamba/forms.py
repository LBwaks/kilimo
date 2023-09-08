from django import forms
from leaflet.forms.widgets import LeafletWidget
from .models import Land, LandCoordiates, LandImages


class LandForm(forms.ModelForm):
    """Form definition for Land."""

    # BOOL_CHOICES = [(True, "Yes"), (False, "No")]
    # show_coordinates = forms.BooleanField(
    #     widget=forms.RadioSelect(choices=BOOL_CHOICES), required=False
    # )

    class Meta:
        """Meta definition for Landform."""

        model = Land
        fields = (
            "title",
            "shamba_id",
            "size",
            "charge",
            "period_lease",
            "category",
            "tags",
            # "climate",
            # "soil_type",
            # "water_source",
            # "electricity_source",
            # "recommended_farming",
            # "existing_infrastructure",
            # "previous_farming",
            # "existing_machinery",
            # "human_labour",
            # "county",
            # "sub_county",
            # "location",
            # "sub_location",
            # "village",
            # "location_coordinates",
        )


class LandResourcesForm(forms.ModelForm):
    """Form definition for Land."""

    class Meta:
        """Meta definition for Landform."""

        model = Land
        fields = (
            "climate",
            "soil_type",
            "water_source",
            "electricity_source",
            "recommended_farming",
        )


class LandInfrastructureForm(forms.ModelForm):
    """Form definition for Land."""

    # BOOL_CHOICES = [(True, "Yes"), (False, "No")]
    # show_coordinates = forms.BooleanField(
    #     widget=forms.RadioSelect(choices=BOOL_CHOICES), required=False
    # )

    class Meta:
        """Meta definition for Landform."""

        model = Land
        fields = (
            "existing_infrastructure",
            "previous_farming",
            "existing_machinery",
            "human_labour",
        )


class LandLocationForm(forms.ModelForm):
    """Form definition for Land."""

    BOOL_CHOICES = [(True, "Yes"), (False, "No")]
    show_coordinates = forms.BooleanField(
        widget=forms.RadioSelect(choices=BOOL_CHOICES), required=False
    )

    class Meta:
        """Meta definition for Landform."""

        model = Land
        fields = (
            "zipcode",
            "county",
            "sub_county",
            "location",
            "sub_location",
            "village",
        )


class LandImagesForm(forms.ModelForm):
    """Form definition for Land."""

    images = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "required": False,
                "class": "form-control images",
                # 'multiple': True
            }
        ),
    )

    class Meta:
        """Meta definition for Landform."""

        model = LandImages
        fields = ("images",)


class LandCoordinatesForm(forms.ModelForm):
    """Form definition for Land."""

    # coordinates = PointField(widget=LeafletWidget())
    class Meta:
        #     """Meta definition for Landform."""

        model = LandCoordiates
        fields = (
            "land",
            "coordinates",
        )
        widgets = {'coordinates': LeafletWidget()}

        #################################################### update forms ###########################


class LandUpdateForm(forms.ModelForm):
    """Form definition for LandUpdate."""

    images = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "required": False,
                "class": "form-control images",
                # 'multiple': True)
            }
        ),
    )

    class Meta:
        """Meta definition for LandUpdateform."""

        model = Land
        fields = (
            "title",
            "shamba_id",
            "size",
            "charge",
            "period_lease",
            "category",
            "tags",
            "climate",
            "soil_type",
            "water_source",
            "electricity_source",
            "recommended_farming",
            "existing_infrastructure",
            "previous_farming",
            "existing_machinery",
            "human_labour",
            "county",
            "sub_county",
            "location",
            "sub_location",
            "village",
            # "location_coordinates",
        )

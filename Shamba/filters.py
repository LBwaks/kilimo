import django_filters
from .models import Land,LandCategory,LandTag,LeasePeriod
from .choices import COUNTY,SUBCOUNTY,LOCATION

class LandFilter(django_filters.FilterSet):
    category=django_filters.ModelChoiceFilter(queryset = LandCategory.objects.all()),
    tags = django_filters.ModelChoiceFilter(queryset =LandTag.objects.all()),
    size = django_filters.RangeFilter(),
    charge=django_filters.RangeFilter(),
    period_lease=django_filters.ModelChoiceFilter(queryset = LeasePeriod.objects.all()),
    county =django_filters.ChoiceFilter(choises = COUNTY),
    sub_county=django_filters.ChoiceFilter(choices=SUBCOUNTY),
    location= django_filters.ChoiceFilter(choices=LOCATION),
    
    class Meta:
        model = Land
        fields = [
            "category",
            "tags",
            "size",
            "charge",
            "period_lease",
            "county",
            "sub_county",
            "location",
        ]

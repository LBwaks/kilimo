import django_filters
from .models import Service,ServiceCategory,ServiceTag
from Shamba.choices import PERIOD,COUNTY

class ServiceFilter(django_filters.FilterSet):
    category=django_filters.ModelChoiceFilter(queryset = ServiceCategory.objects.all()),
    tags = django_filters.ModelChoiceFilter(queryset =ServiceTag.objects.all()),
    # price=django_filters.RangeFilter(),
    period=django_filters.ChoiceFilter(choices=PERIOD),
    # county =django_filters.ChoiceFilter(choises = COUNTY),
    
    class Meta:
        model = Service
        fields =[
            "category",
            "tags",            
            # "price",
            "period",
            # "county",
        ]
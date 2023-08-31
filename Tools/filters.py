import django_filters
from .models import Category,Tag,Tool
from Shamba.choices import COUNTY,PERIOD

class ToolFilter(django_filters.FilterSet):
    category=django_filters.ModelChoiceFilter(queryset = Category.objects.all()),
    tags = django_filters.ModelChoiceFilter(queryset =Tag.objects.all()),
    price=django_filters.RangeFilter(),
    period=django_filters.ChoiceFilter(choices=PERIOD),
    county =django_filters.ChoiceFilter(choises = COUNTY),
    
   
    class Meta:
        model = Tool
        fields =[
            "category",
            "tags",            
            "price",
            "period",
            "county",
            
            
        ]
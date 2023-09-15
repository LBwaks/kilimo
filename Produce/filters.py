import django_filters

from Produce.choices import CONTROL, ORGANIC

from .models import Produce, ProduceCategory, ProduceTag


class ProduceFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset =ProduceCategory.objects.all())
    tags = django_filters.ModelMultipleChoiceFilter(queryset=ProduceTag.objects.all())
    growth_way =django_filters.ChoiceFilter(choices =ORGANIC)
    control_growth = django_filters.ChoiceFilter(choices = CONTROL)
    class Meta:
        model = Produce
        fields = ["category", "tags", "growth_way", "control_growth"]

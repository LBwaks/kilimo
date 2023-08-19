from django.contrib import admin

from .models import LeasePeriod, Land

# Register your models here.


@admin.register(LeasePeriod)
class LeasePeriodAdmin(admin.ModelAdmin):
    """Admin View for LeasePeriod"""

    list_display = ("period", "other_period", "created")
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)


@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    """Admin View for ShAdmin"""

    list_display = ("land_id", "shamba_id", "location_coordinates")
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
    # ordering = ('',)

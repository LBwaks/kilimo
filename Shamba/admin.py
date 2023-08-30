from typing import Any
from django.contrib import admin

from .models import LeasePeriod, Land,LandCategory,LandCoordiates,LandTag

# Register your models here.


@admin.register(LandCategory)
class LandCategoryAdmin(admin.ModelAdmin):
    '''Admin View for LandCategory'''

    list_display = ('type',"is_featured")
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ('user',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)
    
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
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)
    


@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    """Admin View for ShAdmin"""

    list_display = ("title","land_id", "shamba_id", "type")
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
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)
    
@admin.register(LandCoordiates)
class LandCoordiatesAdmin(admin.ModelAdmin):
    '''Admin View for LandCoordiates'''

    list_display = ('land','coordinates','updated','created')
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
@admin.register(LandTag)
class LandTagAdmin(admin.ModelAdmin):
    '''Admin View for LandTag'''

    list_display = ('name','created')
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ('user',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)
from typing import Any
from django.contrib import admin
from .models import Produce,ProduceCategory,ProduceTag
# Register your models here.

@admin.register(ProduceCategory)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ('title','is_published',"is_featured","created")
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

@admin.register(ProduceTag)
class TagAdmin(admin.ModelAdmin):
    '''Admin View for ProduceTag'''

    list_display = ('name','category','is_published','created')
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
        obj.user=request.user
        return super().save_model(request, obj, form, change)

@admin.register(Produce)
class ProduceAdmin(admin.ModelAdmin):
    '''Admin View for Produce'''

    list_display = ('title','category','growth_way','control_growth')
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
    
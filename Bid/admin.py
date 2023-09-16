from typing import Any
from django.contrib import admin
from .models import Bid 

# Register your models here.
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    '''Admin View for Bid'''

    list_display = ('user','produce','charge','status','created')
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('user',)
    readonly_fields = ('user',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)
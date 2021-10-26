from common.admin import JsonAdmin
from django.contrib import admin
from store.models import *

from custom_admin_arrayfield.admin.mixins import DynamicArrayMixin

class StoreAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass

admin.site.register(Store, StoreAdmin)
admin.site.register(PriceTime)
admin.site.register(Event)

@admin.register(Bay)
class BayAdmin(admin.ModelAdmin):
    readonly_fields = ("supported_vehicle_types", )

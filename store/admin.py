from django.contrib import admin
from store.models import *

admin.site.register(Store)
admin.site.register(PriceTime)
admin.site.register(Event)

@admin.register(Bay)
class BayAdmin(admin.ModelAdmin):
    readonly_fields = ("supported_vehicle_types", )

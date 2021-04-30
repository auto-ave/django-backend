from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(VehicleType)
admin.site.register(Store)
admin.site.register(StoreImage)
admin.site.register(PriceTime)
admin.site.register(Event)

@admin.register(Bay)
class BayAdmin(admin.ModelAdmin):
    readonly_fields = ("supported_vehicle_types", )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    readonly_fields = ("supported_vehicle_types", )
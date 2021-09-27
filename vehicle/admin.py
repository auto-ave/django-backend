from django.contrib import admin

from vehicle.models import VehicleBrand, VehicleModel, VehicleType, Wheel

admin.site.register(VehicleType)
admin.site.register(Wheel)

admin.site.register(VehicleBrand)


class VehicleModelAdmin(admin.ModelAdmin):
    list_filter = ('vehicle_type',)

admin.site.register(VehicleModel, VehicleModelAdmin)
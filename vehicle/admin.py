from django.contrib import admin

from vehicle.models import VehicleBrand, VehicleModel, VehicleType, Wheel

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('model', 'wheel')
    list_filter = ( 'wheel', )
    search_fields = ( 'model', )

@admin.register(Wheel)
class WheelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(VehicleBrand)
class VehicleBrandAdmin(admin.ModelAdmin):
    search_fields = ('name', )

@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ('model', 'brand', 'vehicle_type', )
    list_filter = ('vehicle_type',)
    search_fields = ( 'model', 'brand__name' )
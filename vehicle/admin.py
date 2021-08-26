from django.contrib import admin

from vehicle.models import VehicleType, Wheel

admin.site.register(VehicleType)
admin.site.register(Wheel)
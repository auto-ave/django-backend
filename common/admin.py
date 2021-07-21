from django.contrib import admin

from common.models import City, Service

admin.site.register(City)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass
    # readonly_fields = ("supported_vehicle_types", )
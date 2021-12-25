from common.admin import JsonAdmin
from django.contrib import admin
from store.models import *

from custom_admin_arrayfield.admin.mixins import DynamicArrayMixin

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ( 'name', 'slug', 'city', 'owner', 'rating', 'is_active' )
    list_filter = ( 'city', 'is_active', 'is_verified_by_admin', 'is_locked_for_salesman', )
    search_fields = ( 'name', 'slug', 'city__name', 'owner__user__first_name', 'owner__user__last_name' )

@admin.register(PriceTime)
class PriceTimeAdmin(admin.ModelAdmin):
    list_display = ( 'store', 'service', 'vehicle_type', 'price', 'time_interval' )
    list_filter = ( 'store', 'vehicle_type' )
    search_fields = ( 'store__name', 'service__name', )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ( 'bay', 'start_datetime', 'end_datetime', 'is_blocking' )
    list_filter = ( 'is_blocking', )
    search_fields = ( 'bay__store__name', )

@admin.register(Bay)
class BayAdmin(admin.ModelAdmin):
    readonly_fields = ("supported_vehicle_types", )
    list_display = ( 'id', 'store' )
    list_filter = ( 'store', )

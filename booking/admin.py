from django.contrib.admin.decorators import action
from django.utils.html import format_html
from django.contrib import admin
from booking.static import BookingStatusSlug
from .models import *

import datetime

class HiddenFieldsAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('booked_by', 'store'),
        }),
    )
    def get_readonly_fields(self, request, obj=None):
        # try:
        #     return [f.name for f in obj._meta.fields if not f.editable]
        # except:
        #     # if a new object is to be created the try clause will fail due to missing _meta.fields
        #     return ""
        if obj: # editing an existing object
            return ('booked_by', 'store')
        return self.readonly_fields

@admin.register(Booking)
class Booking(HiddenFieldsAdmin):
    list_display = (
        'booking_id', 'store', 'booking_status', 'amount', 'vehicle_model'
    )
    list_filter = ( 'store', 'booking_status')
    search_fields = ('booking_id', 'store__name', 'booking_status__slug', 'vehicle_model__model', 'vehicle_model__brand__name')

admin.site.register(BookingStatus)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(Review)

admin.site.register(Slot)


@admin.action(description="Aprove Cancellation request for the selected Bookings")
def approve_cancellation(modeladmin, request, queryset):
    for cancellation_request in queryset:
        cancellation_request.booking.approve_cancellation_request()

@admin.register(CancellationRequest)
class CancellationRequestAdmin(admin.ModelAdmin):
    list_display = (
        'booking', 'reason', 'cancellation_status',
    )
    list_filter = ('reason',)
    actions = (approve_cancellation,)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'title', 'is_active', 'discount_percentage'
    )
    list_filter = ( 'is_active', 'valid_from', 'valid_to')
    search_fields = ('code', 'title', 'description')

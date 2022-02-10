from django.contrib.admin.decorators import action
from django.http import HttpRequest
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
class BookingAdmin(HiddenFieldsAdmin):
    list_display = ( 'booking_id', 'created_at', 'store', 'booking_status', 'event_start', 'amount', 'vehicle_model' )
    list_filter = ( 'is_multi_day', 'booking_status', 'store', )
    search_fields = ( 'booking_id', 'store__name', 'booking_status__slug', 'vehicle_model__model', 'vehicle_model__brand__name' )

    def event_start(self, obj):
        if hasattr(obj, 'event'):
            return obj.event.start_datetime
        else:
            return '-'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('event', 'vehicle_model', 'store', 'booking_status')


admin.site.register(BookingStatus)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ( 'booking', 'status', 'amount', 'gateway_name', 'bank_name', 'mode_of_payment' )
    list_filter = ( 'mode_of_payment', 'bank_name')
    search_fields = ( 'booking__booking_id', 'booking__store__name', 'bank_name' )

admin.site.register(Refund)
admin.site.register(Review)



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

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'title', 'is_active', 'discount_percentage'
    )
    list_filter = ( 'is_active', 'valid_from', 'valid_to')
    search_fields = ('code', 'title', 'description')

admin.site.register(OfferRedeem)

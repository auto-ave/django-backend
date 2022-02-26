from django.contrib.admin.decorators import action
from django.http import HttpRequest
from django.utils.html import format_html
from django.contrib import admin
from booking.static import BookingStatusSlug
from .models import *
from django.core.exceptions import ValidationError
from easy_select2 import select2_modelform

import datetime

BookingForm = select2_modelform(Booking, attrs={'width': '350px'})
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ( 'booking_id', 'created_at', 'store', 'booking_status', 'event_start', 'amount', 'vehicle_model' )
    list_filter = ( 'is_multi_day', 'booking_status', 'store', )
    search_fields = ( 'booking_id', 'store__name', 'booking_status__slug', 'vehicle_model__model', 'vehicle_model__brand__name' )
    readonly_fields = ('booking_id', 'razorpay_order_id', 'amount', 'otp', 'booked_by', 'store', 'is_multi_day', 'offer', 'vehicle_model', 'price_times', 'event')
    
    # form = BookingForm

    def event_start(self, obj):
        if hasattr(obj, 'event'):
            return obj.event.start_datetime
        else:
            return '-'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('event', 'vehicle_model', 'store', 'booking_status')
    
    def get_object(self, request, object_id, from_field=None):
        queryset = self.get_queryset(request)
        model = queryset.model
        field = model._meta.pk if from_field is None else model._meta.get_field(from_field)
        try:
            object_id = field.to_python(object_id)
            return queryset.get(**{field.name: object_id})
        except (model.DoesNotExist, ValidationError, ValueError):
            return None


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
        # if cancellation_request.approved:
        cancellation_request.booking.approve_cancellation_request()
        cancellation_request.approved = True
        cancellation_request.approved_by = request.user
        cancellation_request.approved_at = datetime.datetime.now()
        cancellation_request.save()

@admin.register(CancellationRequest)
class CancellationRequestAdmin(admin.ModelAdmin):
    list_display = (
        'booking', 'reason', 'cancellation_status', 'approved', 'approved_by', 'approved_at'
    )
    list_filter = ('reason',)
    actions = (approve_cancellation,)


OfferForm = select2_modelform(Offer, attrs={'width': '250px'})
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'title', 'is_active', 'discount_percentage'
    )
    list_filter = ( 'is_active', 'valid_from', 'valid_to')
    search_fields = ('code', 'title', 'description')
    form = OfferForm

admin.site.register(OfferRedeem)

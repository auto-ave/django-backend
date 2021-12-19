from rest_framework import permissions, generics, response
from booking.serializers.cancel import BookingCancelSerializer
from booking.static import BOOKING_CANCEL_PRIOR_HOURS, BOOKING_CANCEL_REASONS, BookingStatusSlug
from booking.models import Booking, BookingStatus, CancellationRequest
from common.mixins import ValidateSerializerMixin
from common.permissions import IsConsumer
from misc.contact_details import CONTACT_EMAIL

import datetime

class BookingCancelData(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        booking_id = kwargs['booking_id']
        booking = Booking.objects.get(booking_id=booking_id)
        
        if booking.booked_by != request.user.consumer:
            return response.Response({
                "error": "You are not allowed to cancel this booking"
            })

        if CancellationRequest.objects.filter(booking=booking).first():
            return response.Response({
                "error": "Cancellation Request has already been submitted for this booking, please feel free to contact us at {} for any further queries.".format(CONTACT_EMAIL)
            })
        
        if booking.booking_status != BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_SUCCESS):
            return response.Response({
                "error": "Invalid Booking status to cancel a booking, check if payment is completed. Please feel free to contact us at {} for any further queries.".format(CONTACT_EMAIL)
            })
        
        current_time = datetime.datetime.now()
        
        is_refundable = False
        refund_amount = 0
        
        if current_time + datetime.timedelta(hours=BOOKING_CANCEL_PRIOR_HOURS) <= booking.event.start_datetime :
            is_refundable = True
            refund_amount = float(booking.payment.amount) # Full refund as currently we only supporting partial payment
        
        reasons = BOOKING_CANCEL_REASONS
        return response.Response({
            "reasons": reasons,
            "refund_amount": refund_amount,
            "is_refundable": is_refundable,
        })

class BookingCancel(generics.GenericAPIView, ValidateSerializerMixin):
    permission_classes = (IsConsumer, )
    serializer_class = BookingCancelSerializer

    def post(self, request, *args, **kwargs):
        data = self.validate(request)
        booking_id = kwargs['booking_id']
        reason = data['reason']
        
        booking = Booking.objects.get(booking_id=booking_id)
        
        if booking.booked_by != request.user.consumer:
            return response.Response({
                "error": "You are not allowed to cancel this booking"
            })

        if CancellationRequest.objects.filter(booking=booking).first():
            return response.Response({
                "error": "Cancellation Request has already been submitted for this booking, please feel free to contact us at {} for any further queries.".format(CONTACT_EMAIL)
            })
        
        if booking.booking_status != BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_SUCCESS):
            return response.Response({
                "error": "Invalid Booking status to cancel a booking, , please feel free to contact us at {} for any further queries.".format(CONTACT_EMAIL)
            })

        CancellationRequest.objects.create(booking=booking, reason=reason)    

        return response.Response({
            "success": "Cancellation Request successfully submitted"
        })
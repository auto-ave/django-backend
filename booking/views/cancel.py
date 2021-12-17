from rest_framework import permissions, generics, response
from booking.serializers.cancel import BookingCancelSerializer
from booking.static import BOOKING_CANCEL_REASONS, BookingStatusSlug
from booking.models import Booking, BookingStatus, CancellationRequest
from common.mixins import ValidateSerializerMixin
from common.permissions import IsConsumer
from misc.contact_details import CONTACT_EMAIL

class BookingCancelData(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        reasons = BOOKING_CANCEL_REASONS
        return response.Response({
            "reasons": reasons
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
        
        if booking.booking_status == BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_SUCCESS):
            return response.Response({
                "error": "Invalid Booking status to cancel a booking, , please feel free to contact us at {} for any further queries.".format(CONTACT_EMAIL)
            })

        CancellationRequest.objects.create(booking=booking, reason=reason)    

        return response.Response({
            "success": "Cancellation Request successfully submitted"
        })
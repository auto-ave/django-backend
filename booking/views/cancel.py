from rest_framework import permissions, generics, response
from booking.static import BOOKING_CANCEL_REASONS

class BookingCancelData(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        reasons = BOOKING_CANCEL_REASONS
        return response.Response({
            "reasons": reasons
        })

class BookingCancel(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        data = self.validate(request)
        booking_id = data['booking_id']
        otp = data['otp']

        booking = Booking.objects.get(booking_id=booking_id)

        if booking.store.owner.user != request.user:
            return response.Response({
                "error": "You are not allowed to start this booking"
            }, status=403)
        
        if booking.otp != otp:
            return response.Response({
                "error": "Invalid OTP"
            }, status=400)

        booking.start_service()

        return response.Response({
            "success": "Booking started"
        })
from rest_framework import generics
from booking.serializers.general import *
from common.permissions import *
from django_filters.rest_framework import DjangoFilterBackend


class BookingListConsumer(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = ( IsConsumer, )

    def get_queryset(self):
        user = self.request.user
        return user.consumer.booking_set.all()

class BookingListPartner(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = ( IsPartner, )

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(store__owner = user.partner)
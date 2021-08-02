from rest_framework import generics

from booking.models import *
from booking.serializers.general import *

from common.permissions import IsConsumer

class BookingsList(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = ( IsConsumer, )

    def get_queryset(self):
        return Booking.objects.filter(booked_by=self.request.user.consumer)

class BookingDetail(generics.RetrieveAPIView):
    lookup_field = 'booking_id'
    serializer_class = BookingDetailSerializer
    permission_classes = ( IsConsumer, )

    def get_queryset(self):
        return Booking.objects.all()
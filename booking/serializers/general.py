from rest_framework import serializers
from rest_framework.utils import field_mapping

from booking.models import *

class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

class BookingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
    fields = "__all__"

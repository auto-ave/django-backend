from rest_framework import serializers
from rest_framework.utils import field_mapping

from booking.models import *

class BookingListSerializer(serializers.ModelSerializer):
    price_times = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = "__all__"
    
    def get_price_times(self, obj):
        price_times = []
        for price_time in obj.price_times.all():
            price_times.append(price_time.service.name)
        return price_times

class BookingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

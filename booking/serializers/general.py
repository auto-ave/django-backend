from rest_framework import serializers
from rest_framework.utils import field_mapping

from booking.models import *
from store.serializers.services import PriceTimeSerializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class BookingListSerializer(serializers.ModelSerializer):
    price_times = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = "__all__"
    
    def get_price_times(self, obj):
        price_times = []
        for price_time in obj.price_times.all():
            price_times.append(price_time.service.name)
        return price_times
    
    def get_amount(self, obj):
        return obj.payment.amount

class BookingDetailSerializer(serializers.ModelSerializer):
    price_times = PriceTimeSerializer(many=True)
    payment = PaymentSerializer()
    class Meta:
        model = Booking
        fields = "__all__"


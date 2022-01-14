from store.serializers.general import EventSerializer, SalesmanStoreListSerializer
from rest_framework import serializers
from rest_framework.utils import field_mapping

from booking.models import *
from booking.serializers.review import ReviewSerializer
from store.serializers.services import PriceTimeSerializer
from vehicle.serializers import VehicleModelSerializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class BookingListSerializer(serializers.ModelSerializer):
    booking_status = serializers.SerializerMethodField()
    price_times = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()
    store = serializers.SerializerMethodField()
    event = EventSerializer()

    class Meta:
        model = Booking
        fields = "__all__"
    
    def get_booking_status(self, obj):
        return obj.get_booking_status_display()
    
    def get_price_times(self, obj):
        price_times = []
        for price_time in obj.price_times.all():
            price_times.append(price_time.service.name)
        return price_times
    
    def get_amount(self, obj):
        return obj.amount
    
    def get_review(self, obj):
        if hasattr(obj, 'review'):
            return ReviewSerializer(obj.review).data
        return None
    
    def get_store(self, obj):
        store = obj.store
        return {
            "name": store.name,
            "address": store.address,
            "thumbnail": store.thumbnail,
        }


class BookingListOwnerSerializer(serializers.ModelSerializer):
    booking_status = serializers.SerializerMethodField()
    booked_by = serializers.SerializerMethodField()
    price_times = PriceTimeSerializer(many=True)
    remaining_amount = serializers.SerializerMethodField()
    event = EventSerializer()
    vehicle_model = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        exclude = ['amount', 'booking_status_changed_time', 'store']
    
    def get_booking_status(self, obj):
        return obj.get_booking_status_display()
    
    def get_remaining_amount(self, obj):
        return str(float(obj.amount) - float(obj.payment.amount))


    def get_booked_by(self, obj):
        return {
            "name": obj.booked_by.user.full_name(),
            "phone": str(obj.booked_by.user.phone)
        }
    
    def get_vehicle_model(self, obj):
        vehicle = obj.vehicle_model
        return VehicleModelSerializer(vehicle).data
    

class NewBookingListOwnerSerializer(serializers.Serializer):
    date = serializers.DateField()


class BookingDetailSerializer(serializers.ModelSerializer):
    booking_status = serializers.SerializerMethodField()
    price_times = PriceTimeSerializer(many=True)
    payment = PaymentSerializer()
    event = EventSerializer()
    review = serializers.SerializerMethodField()
    store = SalesmanStoreListSerializer()
    vehicle_model = VehicleModelSerializer()
    remaining_amount = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = "__all__"

    def get_review(self, obj):
        if hasattr(obj, 'review'):
            return ReviewSerializer(obj.review).data
        return None
    
    def get_remaining_amount(self, obj):
        return str(float(obj.amount) - float(obj.payment.amount))

    def get_booking_status(self, obj):
        return obj.get_booking_status_display()

class BookingStartSerializer(serializers.Serializer):
    booking_id = serializers.CharField()
    otp = serializers.CharField()

class BookingCompleteSerializer(serializers.Serializer):
    booking_id = serializers.CharField()

class OwnerRevenueSerializer(serializers.Serializer):
    pass
class OwnerStoreVehicleTypesSerializer(serializers.Serializer):
    pass
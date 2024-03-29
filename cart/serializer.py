from django.contrib.postgres import fields
from rest_framework import serializers
from booking.serializers.offer import OfferListSerializer
from common.utils import minutes_to_time_string

from vehicle.serializers import VehicleTypeSerializer
from cart.models import Cart
from store.models import PriceTime
from vehicle.models import VehicleModel
from vehicle.serializers import VehicleModelSerializer

class CartItemSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    time_interval = serializers.SerializerMethodField()
    class Meta:
        model = PriceTime
        exclude = ("description", "store", 'vehicle_type',)
    
    def get_service(self, obj):
        return obj.service.name
    
    def get_time_interval(self, obj):
        return minutes_to_time_string(obj.time_interval)

class CartSerializer(serializers.ModelSerializer):
    item_objs = serializers.SerializerMethodField()
    store = serializers.SerializerMethodField()
    vehicle_model = serializers.SerializerMethodField()
    offer = OfferListSerializer()
    is_multi_day = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = "__all__"
    
    def get_item_objs(self, obj):
        serializer = CartItemSerializer(obj.items.all(), many=True)
        return serializer.data
    
    def get_store(self, obj):
        if obj.store:
            return {
                "id": obj.store.id,
                "name": obj.store.name,
            }
        else:
            return None
    
    def get_vehicle_model(self, obj):
        if obj.vehicle_model:
            serializer = VehicleModelSerializer(obj.vehicle_model)
            return serializer.data
        else:
            return None
    
    def get_is_multi_day(self, obj):
        return obj.is_multi_day()


class FullCartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = "__all__"


class CartAddItemSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=PriceTime.objects.all())
    vehicle_model = serializers.PrimaryKeyRelatedField(queryset=VehicleModel.objects.all())

class CartRemoveItemSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=PriceTime.objects.all())

class ClearCartSerializer(serializers.Serializer):
    pass
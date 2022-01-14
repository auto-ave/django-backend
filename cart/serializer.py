from django.contrib.postgres import fields
from rest_framework import serializers

from vehicle.serializers import VehicleTypeSerializer
from cart.models import Cart
from store.models import PriceTime
from vehicle.models import VehicleModel
from vehicle.serializers import VehicleModelSerializer

class CartItemSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    class Meta:
        model = PriceTime
        exclude = ("description", )
    
    def get_service(self, obj):
        return obj.service.name

class CartSerializer(serializers.ModelSerializer):
    item_objs = serializers.SerializerMethodField()
    store = serializers.SerializerMethodField()
    vehicle_type = serializers.SerializerMethodField()
    vehicle_model = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = "__all__"
    
    def get_item_objs(self, obj):
        serializer = CartItemSerializer(obj.items, many=True)
        return serializer.data
    
    def get_store(self, obj):
        if obj.store:
            return {
                "id": obj.store.id,
                "name": obj.store.name,
            }
        else:
            return None
    
    def get_vehicle_type(self, obj):
        if obj.items.all().first():
            return VehicleTypeSerializer(obj.items.all().first().vehicle_type).data
        else:
            return None
    
    def get_vehicle_model(self, obj):
        if obj.vehicle_model:
            serializer = VehicleModelSerializer(obj.vehicle_model)
            return serializer.data
        else:
            return None


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
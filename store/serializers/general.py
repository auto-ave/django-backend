from common import fields
from rest_framework import serializers, response, status
from rest_framework.serializers import ModelSerializer

from store.models import *


class StoreSerializer(ModelSerializer):
    rating_count = serializers.SerializerMethodField()
    services_start = serializers.SerializerMethodField()

    class Meta():
        model = Store
        fields = "__all__"

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def get_rating_count(self, obj):
        return obj.reviews.all().count()
    
    def get_services_start(self, obj):
        return 499

class StoreListSerializer(ModelSerializer):
    distance = serializers.SerializerMethodField()
    services_start = serializers.SerializerMethodField()

    class Meta():
        model = Store
        fields = ("pk", "slug", "name", "thumbnail", "images", "rating", "distance", "services_start", 'address')

    def get_distance(self, obj):
        latitude = self.context['request'].query_params.get('latitude')
        longitude = self.context['request'].query_params.get('longitude')
        if latitude and longitude:
            return "69 km"
            # return distance(latitude, longitude)
        return '3 km'
    
    def get_services_start(self, obj):
        return 499

class SalesmanStoreListSerializer(ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'address', 'thumbnail', 'slug')
    
class EventSerializer(ModelSerializer):
    class Meta():
        model = Event
        fields = "__all__"


class StoreCreateSerializer(ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    bay_number = serializers.IntegerField(required=True)
    # name = serializers.CharField(max_length=100)
    # store_times = ArrayField(base_field=JSONField())
    # images = ArrayField(base_field=models.URLField(), null=True, blank=True)
    # address = serializers.CharField(max_length=200) #doubt
    # pincode = serializers.CharField(max_length=5)
    # description = serializers.CharField(max_length=300)
    # latitude = serializers.DecimalField(max_digits=22, decimal_places=16)
    # longitude = serializers.DecimalField(max_digits=22, decimal_places=16)
    class Meta():
        model = Store
        exclude = ('is_active', 'created_at', 'updated_at', 'is_verified_by_admin', 'is_locked_for_salesman', 'partner', 'owner', 'salesman', 'supported_vehicle_types', 'rating')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.validated_data)
        return response.Response(serializer.validate_data, status=status.HTTP_201_CREATED, headers=headers)

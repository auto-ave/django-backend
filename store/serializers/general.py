from django.shortcuts import get_object_or_404
from common import fields
from rest_framework import serializers, response, status
from rest_framework.serializers import ModelSerializer
from common.models import ServiceTag
from common.utils import distanceFromLatitudeAndLongitude
from store.models import *
from store.serializers.services import PriceTimeListSerializer, StoreListPriceTimeSerializer


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
        pricetimes = obj.pricetimes.filter(is_offer=False)
        min = 999999
        for pricetime in pricetimes:
            if pricetime.price <= min:
                min = pricetime.price
        if min == 999999:
            return 499
        else:
            return min

class StoreDetailOwnerSerializer(ModelSerializer):
    class Meta():
        model = Store
        fields = ( 'name', 'address', 'thumbnail', )

class StoreListSerializer(ModelSerializer):
    distance = serializers.SerializerMethodField()
    services_start = serializers.SerializerMethodField()
    tagged_services = serializers.SerializerMethodField()

    class Meta():
        model = Store
        fields = ("pk", "slug", "name", "thumbnail", "images", "rating", "distance", "services_start", 'address', 'tagged_services')

    def get_distance(self, obj):
        latitude = self.context['request'].query_params.get('latitude')
        longitude = self.context['request'].query_params.get('longitude')
        store_latitude = obj.latitude
        store_longitude = obj.longitude
        if latitude and longitude:
            return distanceStringFromLatitudeAndLongitude(latitude, longitude, store_latitude, store_longitude)

        return None
    
    def get_services_start(self, obj):
        tag = self.context['request'].query_params.get('tag')
        sort = self.context['request'].query_params.get('sort')
        if tag or sort:
            return None
        else:
            pricetimes = obj.pricetimes.filter(is_offer=False)
            min = 999999
            for pricetime in pricetimes:
                if pricetime.price <= min:
                    min = pricetime.price
            if min == 999999:
                return 499
            else:
                return min
    
    def get_tagged_services(self, obj):
        tag = self.context.get('tag', None)
        services = self.context.get('services', None)
        
        vehicle_model = self.context['request'].query_params.get('vehicle_model')
        
        final_pricetimes = []
        if services or tag:
            price_times = obj.pricetimes.prefetch_related('service').filter(
                service__in=services, is_offer=False
            )
            for service in services:
                # TODO: only filter 4 wheeler prices
                # price_times = obj.pricetimes.filter(
                #     service=service
                # ).prefetch_related('service')
                filtered_pricetimes = list( filter( lambda pricetime: pricetime.service.id == service.id , price_times ) )
                final_pricetimes.extend(filtered_pricetimes)
                # if len(filtered_pricetimes):
                #     pricetime = filtered_pricetimes[0]
                #     final_pricetimes.append(f'{pricetime.service.name} starting at ₹{pricetime.price}')
                #     break
        return StoreListPriceTimeSerializer(final_pricetimes, many=True).data

class SalesmanStoreListSerializer(ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'address', 'thumbnail', 'images', 'slug', 'latitude', 'longitude', 'contact_person_name', 'contact_person_number', 'created_at', 'updated_at', 'is_active', 'is_verified_by_admin', 'is_locked_for_salesman')
    
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
        exclude = ('created_at', 'updated_at', 'is_verified_by_admin', 'is_locked_for_salesman', 'partner', 'owner', 'salesman', 'supported_vehicle_types', 'rating')

class StoreUpdateSerializer(ModelSerializer):
    class Meta():
        model = Store
        fields = ('thumbnail', 'images' )


class StorePriceTimeListSerializer(serializers.Serializer):
    pass

class StoreRegistrationEmailSerializer(serializers.Serializer):
    pass

class ServiceCreationDetailsSerializer(serializers.Serializer):
    pass

class SalesmanStoreServiceRetrieveSerializer(serializers.Serializer):
    pass
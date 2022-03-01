from rest_framework import serializers

from common.models import City, Service, ServiceTag

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

class ServiceTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTag
        fields = "__all__"

class StoreServiceListTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTag
        fields = ( 'name', 'slug' )

class CityListSerializer(serializers.Serializer):
    pass
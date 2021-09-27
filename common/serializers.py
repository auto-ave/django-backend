from rest_framework import serializers

from common.models import City, Service

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

class CouponVerifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100)
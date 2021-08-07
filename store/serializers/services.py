from rest_framework import serializers
from store.models import PriceTime, Service

class PriceTimeListSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()

    def get_service(self, obj):
        return obj.service.name

    class Meta:
        model = PriceTime
        fields = "__all__"

class PriceTimeSerializer(serializers.ModelSerializer):
    service = serializers.SerializerMethodField()
    class Meta:
        model = PriceTime
        fields = "__all__"
    
    def get_service(self, obj):
        return obj.service.name

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"
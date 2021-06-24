from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import *


class StoreSerializer(ModelSerializer):
    class Meta():
        model = Store
        fields = "__all__"

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class StoreListSerializer(ModelSerializer):
    distance = serializers.SerializerMethodField()
    services_start = serializers.SerializerMethodField()
    class Meta():
        model = Store
        fields = ("pk", "name", "thumbnail", "rating", "distance", "services_start")

    def get_distance(self, obj):
        return '3 km'
    
    def get_services_start(self, obj):
        return 499
    

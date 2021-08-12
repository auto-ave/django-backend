from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import *


class StoreSerializer(ModelSerializer):
    rating_count = serializers.SerializerMethodField()

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

class StoreListSerializer(ModelSerializer):
    distance = serializers.SerializerMethodField()
    services_start = serializers.SerializerMethodField()
    class Meta():
        model = Store
        fields = ("pk", "slug", "name", "thumbnail", "rating", "distance", "services_start")

    def get_distance(self, obj):
        return '3 km'
    
    def get_services_start(self, obj):
        return 499
    
class EventSerializer(ModelSerializer):
    class Meta():
        model = Event
        fields = "__all__"


class StoreGeneralSerializer(ModelSerializer):

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
        fields = "__all__"



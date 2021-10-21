from rest_framework import serializers
from vehicle.models import VehicleBrand, VehicleModel, VehicleType
from vehicle.serializers import VehicleBrandSerializer

class VehicleTypePopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'

class VehicleModelPopulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = '__all__'


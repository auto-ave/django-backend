from rest_framework import serializers

from vehicle.models import VehicleType

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        exclude = ('created_at', 'updated_at')
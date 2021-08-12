from rest_framework import serializers

from vehicle.models import VehicleType

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = "__all__"
from rest_framework import serializers

from vehicle.models import VehicleType

class VehicleTypeSerializer(serializers.ModelSerializer):
    wheel = serializers.SerializerMethodField()
    class Meta:
        model = VehicleType
        exclude = ('created_at', 'updated_at')
    
    def get_wheel(self, obj):
        if obj.wheel:
            return obj.wheel.name
        return None
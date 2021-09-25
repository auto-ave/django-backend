from rest_framework import fields, serializers

from vehicle.models import VehicleType, Wheel, VehicleBrand, VehicleModel

class VehicleTypeSerializer(serializers.ModelSerializer):
    wheel = serializers.SerializerMethodField()
    class Meta:
        model = VehicleType
        exclude = ('created_at', 'updated_at')
    
    def get_wheel(self, obj):
        if obj.wheel:
            return obj.wheel.name
        return None

class WheelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wheel
        fields = "__all__"

class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = "__all__"

class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = "__all__"
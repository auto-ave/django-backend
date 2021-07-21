from rest_framework import serializers

from misc.models import StoreImage, ServiceImage

class StoreImageSerializer(serializers.Serializer):
    store = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.FileField(read_only=True)

class ServiceImageSerializer(serializers.Serializer):
    service = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.FileField(read_only=True)
    
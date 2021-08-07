from rest_framework import serializers
class ImageSerializer(serializers.Serializer):
    image = serializers.FileField(read_only=True)

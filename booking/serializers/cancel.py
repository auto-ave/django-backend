from rest_framework import serializers

class BookingCancelDataSerializer(serializers.Serializer):
    pass

class BookingCancelSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=500)

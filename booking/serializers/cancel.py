from rest_framework import serializers

class BookingCancelSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=500)
from rest_framework import serializers

class GetOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10)
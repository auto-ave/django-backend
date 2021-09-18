from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

class GetOTPSerializer(serializers.Serializer):
    phone = PhoneNumberField()

class CheckOTPSerializer(serializers.Serializer):
    phone = PhoneNumberField()
    otp = serializers.CharField(max_length=4)
    token = serializers.CharField()

class AppLogoutSerializer(serializers.Serializer):
    token = serializers.CharField()

class CredentialLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
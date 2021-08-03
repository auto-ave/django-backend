from rest_framework import generics, response, status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from accounts.models import User, Consumer
from accounts.serializers.auth import *
from common.mixins import ValidateSerializerMixin

from rest_framework_simplejwt.tokens import RefreshToken

class AuthGetOTP(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = GetOTPSerializer

    def post(self, request, *args, **kwargs):
        data = self.validate(request)
        phone = data.get('phone')

        user = User.objects.filter(Q(phone=phone) | Q(username=phone)).first()
        created = False
        if not user:
            created = True
            user = User.objects.create(phone=phone, username=phone)
            Consumer.objects.create(user=user)

        user.generate_otp()

        return response.Response({
            "created": created
        }, status=status.HTTP_200_OK)

class AuthCheckOTP(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = CheckOTPSerializer

    def post(self, request, *args, **kwargs):
        data = self.validate(request)
        phone = data.get('phone')
        otp = data.get('otp')

        user = get_object_or_404(User, phone=phone)
        if user.check_otp(otp):
            refresh = RefreshToken.for_user(user)
            return response.Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return response.Response({
                "detail": "Invalid OTP"
            }, status=status.HTTP_400_BAD_REQUEST)
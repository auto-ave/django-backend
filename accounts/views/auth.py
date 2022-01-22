from rest_framework import generics, response, status, permissions
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Q
from accounts.models import User, Consumer
from cart.models import Cart
from accounts.serializers.auth import *
from common.communication_provider import CommunicationProvider
from common.mixins import ValidateSerializerMixin
from fcm_django.models import FCMDevice

from rest_framework_simplejwt.tokens import RefreshToken

from misc.sms_contents import SMS_LOGIN_CONTENT
from motorwash.exception_handler import ResponseData, StatusCode
from motorwash.throttles import OTPBurst, OTPRate, OTPSustained

import time

class AuthGetOTP(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = GetOTPSerializer
    throttle_classes = [ OTPBurst, OTPSustained, OTPRate ]

    def post(self, request, *args, **kwargs):
        data = self.validate(request)
        phone = data.get('phone')

        user = User.objects.filter(Q(phone=phone) | Q(username=phone)).first()
        created = False
        if not user:
            created = True
            user = User.objects.create(phone=phone, username=phone)
            consumer = Consumer.objects.create(user=user)
            Cart.objects.create(consumer=consumer)
        if not user.is_consumer():
            consumer = Consumer.objects.create(user=user)
            Cart.objects.create(consumer=consumer)
        try:
            if settings.DEBUG:
                user.otp = '1234'
                user.save()
            else:
                user.generate_otp()
                if settings.FAST2SMS_ENABLE:
                    CommunicationProvider().send_sms(
                        **SMS_LOGIN_CONTENT(user)
                    )
        except Exception as e:
            return response.Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return response.Response({
            "created": created
        }, status=status.HTTP_200_OK)

class AuthCheckOTP(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = CheckOTPSerializer
    # throttle_scope = 'public_get_api'

    def post(self, request, *args, **kwargs):
        # start_time = time.time()
        data = self.validate(request)
        phone = data.get('phone')
        otp = data.get('otp')
        token = data.get('token')
        # print('data mil gaya: ', time.time() - start_time)

        user = get_object_or_404(User, phone=phone)
        # print('user nikal liya: ', time.time() - start_time)
        if user.check_otp(otp):
            # print('otp check karliya: ', time.time() - start_time)
            if token:
                user.register_fcm(user.id, token)
                # print('token register karliya: ', time.time() - start_time)

            refresh = RefreshToken.for_user(user)
            # print('refrest token bana liya, sending response now: ', time.time() - start_time)
            return response.Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return response.Response(
                ResponseData(
                    StatusCode.FAIL,
                    'OTP is incorrect'
                ).to_dict()
            , status=status.HTTP_400_BAD_REQUEST)

class AppLogout(generics.GenericAPIView, ValidateSerializerMixin):
    permission_classes = ( permissions.IsAuthenticated, )
    serializer_class = AppLogoutSerializer

    def post(self, request):
        data = self.validate(request)
        user = request.user
        token = data.get('token')

        if token:
            user.deregister_fcm(user.id, token)
                
        return response.Response({
            'success': True
        })

class SalesmanLogin(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = CredentialLoginSerializer

    def post(self, request):
        data = self.validate(request)
        email = data.get('email')
        password = data.get('password')

        user = get_object_or_404(User, email=email)

        if not user.is_salesman():
            return response.Response({
                "detail": "User is not a salesman"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return response.Response({
                "detail": "Invalid Password"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        return response.Response(user.get_auth_tokens(), status=status.HTTP_200_OK)

class StoreOwnerLogin(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = CredentialLoginSerializer

    def post(self, request):
        data = self.validate(request)
        email = data.get('email')
        password = data.get('password')
        token = data.get('token')

        user = get_object_or_404(User, email=email)

        if not user.is_store_owner():
            return response.Response({
                "detail": "User is not a store owner"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return response.Response({
                "detail": "Invalid Password"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if token:
            user.register_fcm(user.id, token)
            
        return response.Response(user.get_auth_tokens(), status=status.HTTP_200_OK)
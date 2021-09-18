from rest_framework import generics, response, status, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Q
from accounts.models import User, Consumer
from cart.models import Cart
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
            consumer = Consumer.objects.create(user=user)
            Cart.objects.create(consumer=consumer)
        try:
            user.send_otp()
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

    def post(self, request, *args, **kwargs):
        data = self.validate(request)
        phone = data.get('phone')
        otp = data.get('otp')
        token = data.get('token')

        user = get_object_or_404(User, phone=phone)
        if user.check_otp(otp):
            # Adding fcm token to user's tokens
            user.fcm_tokens = list(set(user.fcm_tokens + [token]))
            user.save()

            # subsubscribing token to user's topics

            refresh = RefreshToken.for_user(user)
            return response.Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return response.Response({
                "detail": "Invalid OTP"
            }, status=status.HTTP_400_BAD_REQUEST)

class AppLogout(generics.GenericAPIView, ValidateSerializerMixin):
    permission_classes = ( permissions.IsAuthenticated, )
    serializer_class = AppLogoutSerializer

    def post(self, request):
        data = self.validate(request)
        user = request.user
        token = data['token']

        # firebase messaging fcm token unsubscribe from all the topics of the user
        

        # remove token from users fcm token list
        user.fcm_tokens = [t for t in user.fcm_tokens if t != token]
        user.save()

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

        user = get_object_or_404(User, email=email)

        if not user.is_store_owner():
            return response.Response({
                "detail": "User is not a store owner"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return response.Response({
                "detail": "Invalid Password"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        return response.Response(user.get_auth_tokens(), status=status.HTTP_200_OK)
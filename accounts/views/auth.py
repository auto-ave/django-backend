from rest_framework import generics, response

from accounts.serializers.auth import *
from common.mixins import ValidateSerializerMixin

class AuthGetOTP(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = GetOTPSerializer

    def post(self, request, *args, **kwargs):
        data = self.validate()
        print(data)
        return response.Response({
            "hello": "dfsdf"
        })
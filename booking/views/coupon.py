from django.db.models import query
from rest_framework import generics, response
from common.mixins import ValidateSerializerMixin
from common.permissions import *
from booking.models import Coupon
from booking.serializers.coupon import *


class CouponListView(generics.ListAPIView):
    serializer_class = CouponSerializer
    permission_classes = (IsConsumer,)
    queryset = Coupon.objects.active_coupons()

class CouponApplyView(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = CouponApplySerializer
    permission_classes = (IsConsumer,)
    
    def post(self, request, *args, **kwargs):
        data = self.validate(request)
        user = request.user
        
        code = data.get('code')
        cart = user.consumer.get_cart()
        
        
        return response.Response({})
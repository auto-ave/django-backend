from rest_framework import serializers
from booking.models import Coupon

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

class CouponApplySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=21)
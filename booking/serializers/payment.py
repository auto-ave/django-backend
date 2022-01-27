from booking.models import Payment
from rest_framework import serializers

from store.models import Bay

class PaymentChoicesSerializer(serializers.Serializer):
    pass

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class InitiateTransactionSerializer(serializers.Serializer):
    date = serializers.DateField()
    bay = serializers.PrimaryKeyRelatedField(queryset=Bay.objects.all(), required=False, allow_null=True, default=None)
    slot_start = serializers.TimeField()
    slot_end = serializers.TimeField(required=False, allow_null=True, default=None)

class RazorPayPaymentCallbackSerializer(serializers.Serializer):
    booking_id = serializers.CharField()
    razorpay_order_id = serializers.CharField(required=False, allow_null=True, default=None)
    razorpay_payment_id = serializers.CharField(required=False, allow_null=True, default=None)
    razorpay_signature = serializers.CharField(required=False, allow_null=True, default=None)
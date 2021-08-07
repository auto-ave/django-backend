from booking.models import Payment
from rest_framework import serializers

from store.models import Bay

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class InitiateTransactionSerializer(serializers.Serializer):
    date = serializers.DateField()
    bay = serializers.PrimaryKeyRelatedField(queryset=Bay.objects.all())
    slot_start = serializers.TimeField()
    slot_end = serializers.TimeField()
    
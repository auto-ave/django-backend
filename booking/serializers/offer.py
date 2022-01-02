from rest_framework import serializers
from booking.models import Offer

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

class OfferApplySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=21)
from rest_framework import serializers
from booking.models import Offer

class OfferListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        exclude = ('discount_percentage', 'max_discount', 'max_redeem_count', 'max_redeem_count_per_cosumer', 'valid_from', 'valid_to')

class OfferBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('code', 'banner')

class OfferApplySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=21)

class OfferRemoveSerializer(serializers.Serializer):
    pass
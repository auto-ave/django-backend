from django.contrib.postgres import fields
from rest_framework import serializers

from cart.models import Cart
from store.models import PriceTime

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"

class ItemSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=PriceTime.objects.all())
from rest_framework import serializers

from cart.models import Cart

class SlotCreateSerializer(serializers.Serializer):
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())
    date = serializers.DateField()
    
        

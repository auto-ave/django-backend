from rest_framework import serializers

from cart.models import Cart

class SlotCreateSerializer(serializers.Serializer):
    date = serializers.DateField()
    
        

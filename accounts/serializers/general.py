from rest_framework import serializers 
from django.contrib.auth import get_user_model

from accounts.models import *


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    # is_confirmed = serializers.SerializerMethodField()
    # is_phone_verified = serializers.SerializerMethodField()
    class Meta:
        model = get_user_model()
        fields = ['id','phone', 'is_sub_admin' ,'is_support','is_consumer','is_salesman','is_partner']
        depth = 1
    
    def get_id(self, obj):
        if obj.is_consumer:
            return obj.consumer.id
        if obj.is_partner:
            return obj.partner.id
        if obj.is_salesman:
            return obj.salesman.id
        if obj.is_sub_admin:
            return obj.subadmin.id
        if obj.is_support:
            return obj.support.id    
        return None
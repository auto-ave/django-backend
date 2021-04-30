from rest_framework.serializers import ModelSerializer

from store.models import *


class StoreSerializer(ModelSerializer):
    class Meta():
        model = Store
        fields = "__all__"
from rest_framework.serializers import ModelSerializer

from store.models import *


class StoreSerializer(ModelSerializer):
    class Meta():
        model = Store
        fields = "__all__"

class StoreListSerializer(ModelSerializer):
    class Meta():
        model = Store
        fields = ("pk", "name", "thumbnail", "address", "store_opening_time", "store_closing_time")
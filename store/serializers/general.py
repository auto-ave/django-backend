from rest_framework.serializers import ModelSerializer

from store.models import *


class StoreSerializer(ModelSerializer):
    class Meta():
        model = Store
        fields = "__all__"

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class StoreListSerializer(ModelSerializer):
    class Meta():
        model = Store
        fields = ("pk", "name", "thumbnail", "address", "store_opening_time", "store_closing_time")
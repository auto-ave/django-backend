from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField

from booking.models import *

class ReviewCreateSerializer(ModelSerializer):
    class Meta():
        model = Review
        exclude = ("consumer", )

class ReviewSerializer(ModelSerializer):
    # TODO After addiong Consumer serializer, uncomment this
    # consumer = COnsumerSerializer()
    user = SerializerMethodField()
    def get_user(self, obj):
        return obj.consumer.user.username
    class Meta():
        model = Review
        fields = "__all__"
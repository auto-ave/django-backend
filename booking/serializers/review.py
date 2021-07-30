from rest_framework.serializers import ModelSerializer

from booking.models import *

class ReviewCreateSerializer(ModelSerializer):
    class Meta():
        model = Review
        exclude = ("consumer", )

class ReviewSerializer(ModelSerializer):
    # TODO After addiong Consumer serializer, uncomment this
    # consumer = COnsumerSerializer()
    class Meta():
        model = Review
        fields = "__all__"
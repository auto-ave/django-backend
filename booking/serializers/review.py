from rest_framework.serializers import ModelSerializer, SerializerMethodField

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
        return "{} {}".format(obj.consumer.user.first_name, obj.consumer.user.last_name) 
    class Meta():
        model = Review
        fields = "__all__"

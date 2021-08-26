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
    image = SerializerMethodField()
    
    class Meta():
        model = Review
        fields = "__all__"

    def get_user(self, obj):
        full_name = obj.consumer.user.full_name()
        if full_name.split():
            return full_name
        else:
            return 'Owner of {}'.format(obj.booking.vehicle_type.model)
    
    def get_image(self, obj):
        return obj.booking.vehicle_type.image

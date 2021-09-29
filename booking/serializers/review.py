from rest_framework.serializers import ModelSerializer, SerializerMethodField

from booking.models import *

class ReviewCreateSerializer(ModelSerializer):
    class Meta():
        model = Review
        exclude = ("consumer", )

class ReviewSerializer(ModelSerializer):
    user = SerializerMethodField()
    image = SerializerMethodField()
    
    class Meta():
        model = Review
        fields = "__all__"

    def get_user(self, obj):
        full_name = obj.consumer.user.full_name()
        if full_name.split():
            return full_name
        elif obj.booking.vehicle_model:
            return 'Owner of {}'.format(obj.booking.vehicle_model.model)
        else:
            return 'Subodh is god, bow before him please'
    
    def get_image(self, obj):
        if obj.booking.vehicle_model:
            return obj.booking.vehicle_model.image
        else:
            return 'https://sc04.alicdn.com/kf/Ha82ad175ce684ea69331b07c244895f87.jpg'


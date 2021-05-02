from rest_framework.serializers import ModelSerializer

from booking.models import *

class BookingSerializer(ModelSerializer):
    class Meta():
        model = Booking
        fields = "__all__"
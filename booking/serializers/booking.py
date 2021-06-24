from rest_framework.serializers import ModelSerializer

from booking.models import *

class BookingCreateSerializer(ModelSerializer):
    
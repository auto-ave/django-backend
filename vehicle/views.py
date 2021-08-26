from vehicle.serializers import VehicleTypeSerializer

from rest_framework import generics
from vehicle.models import VehicleType


class VehicleTypeListView(generics.ListAPIView):
    serializer_class = VehicleTypeSerializer

    def get_queryset(self):
        return VehicleType.objects.all()
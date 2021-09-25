from vehicle.serializers import *

from rest_framework import generics, filters
from vehicle.models import *


class VehicleTypeListView(generics.ListAPIView):
    serializer_class = VehicleTypeSerializer

    def get_queryset(self):
        return VehicleType.objects.all()

class VehicleBrandsListView(generics.ListAPIView):
    serializer_class = VehicleBrandSerializer

    def get_queryset(self):
        return VehicleBrand.objects.all()

class VehicleModelsListView(generics.ListAPIView):
    serializer_class = VehicleModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=brand__name', ]

    def get_queryset(self):
        query = self.request.query_params
        if query:
            return VehicleModel.objects.all()
        else:
            return VehicleModel.objects.none()

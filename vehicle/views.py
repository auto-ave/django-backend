from vehicle.serializers import *

from rest_framework import generics, filters
from vehicle.models import *


class VehicleTypeListView(generics.ListAPIView):
    serializer_class = VehicleTypeSerializer

    def get_queryset(self):
        return VehicleType.objects.all()

class WheelListView(generics.ListAPIView):
    serializer_class = WheelSerializer

    def get_queryset(self):
        return Wheel.objects.all()

class VehicleBrandsListView(generics.ListAPIView):
    serializer_class = VehicleBrandSerializer

    def get_queryset(self):
        wheel = self.request.query_params.get('wheel', None)
        queryset = VehicleBrand.objects.all()
        result = []
        for brand in queryset:
            for model in brand.vehicle_models.all():
                if model.vehicle_type.wheel.code == wheel:
                    result.append(brand)
                    break
        return result

class VehicleModelsListView(generics.ListAPIView):
    serializer_class = VehicleModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=brand__name', ]

    def get_queryset(self):
        brand = self.request.query_params.get('brand')
        if brand:
            return VehicleModel.objects.filter(brand__name__iexact=brand)
        else:
            return VehicleModel.objects.none()

from rest_framework import generics, status
from common.permissions import *

from store.models import *
from store.serializers.general import *
import haversine as hs
from haversine import Unit
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from geopy.geocoders import Nominatim, Photon
from rest_framework.response import Response


class StoreDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.all()

class StoreList(generics.ListAPIView):
    permission_classes = (ReadOnly | IsConsumer, )
    serializer_class = StoreListSerializer

    def get_queryset(self):
        try:
            longitude = float(self.request.query_params.get('longitude'))
            latitude= float(self.request.query_params.get('latitude'))
            vehicle_model = self.request.query_params.get('vehicle')
            geolocator = Photon(user_agent="the_motor_wash")
            location = geolocator.reverse(str(latitude)+","+str(longitude))
            city_name = location.raw['properties']['city']
            city = get_object_or_404(City, name=city_name)
            loc1 = (latitude, longitude)
            vehicle_type = get_object_or_404(VehicleType, vehicle_model = vehicle_model)
            queryset = []
            stores = vehicle_type.stores.filter(city=city)
            for store in stores:
                loc2 = (store.latitude, store.longitude)
                if hs.haversine(loc1, loc2, Unit.METERS) <= 100000:
                    queryset.append(store)
            return queryset
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CityStoreList(generics.ListAPIView):
    permission_classes = (ReadOnly | IsConsumer,)   
    serializer_class = StoreListSerializer
    filterset_fields = ['supported_vehicle_types',]

    def get_queryset(self):
        citycode = self.kwargs['citycode']
        city = get_object_or_404(City, code__iexact=citycode)
        queryset = city.stores.all()
        # if self.request.query_params.get('vehicle_model'):
        #     vehicle_model = self.request.query_params.get('vehicle_model')
        #     vehicle_type = get_object_or_404(VehicleType, model = vehicle_model)
        #     queryset = queryset.filter(supported_vehicle_types__in=[vehicle_type])
        return queryset
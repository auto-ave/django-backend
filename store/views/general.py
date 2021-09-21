from rest_framework import generics, status, filters, response
from common.permissions import *

from store.models import *
from store.serializers.general import *
import haversine as hs
from haversine import Unit
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from geopy.geocoders import Nominatim, Photon
from rest_framework.response import Response
from store.serializers.services import *
import json


class StoreDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.all()
    
    def get_object(self):
        instance = super().get_object()

        # subscribe to store topic
        user = self.request.user
        user.sub_to_topic(instance.slug)\

        return instance

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
    filterset_fields = ['services', ]
    # filter_backends = (filters.SearchFilter,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    

    def get_queryset(self):
        citycode = self.kwargs['citycode']
        city = get_object_or_404(City, code__iexact=citycode)

        # subscribe user to city topic
        user = self.request.user
        user.sub_to_topic(city.slug)

        queryset = city.stores.all()
        return queryset 


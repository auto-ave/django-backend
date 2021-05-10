from rest_framework import generics
from common.permissions import *

from store.models import *
from store.serializers.general import *
import haversine as hs
from haversine import Unit
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from geopy.geocoders import Nominatim, Photon
class StoreDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ( ReadOnly | ( IsPartner & IsStoreOwner ) , )
    def get_queryset(self):
        # user = self.request.user
        # params = self.request.query_params

        # partner_query =  params.get('partner')

        # if partner_query:
        #     partners = Partner.objects.filter(pk=partner_query)
        #     if not partners:
        #         return []
        #     return Store.objects.filter(owner=partner)
        
        return Store.objects.all()

    def get_serializer_class(self):
        return StoreSerializer

class StoreList(generics.ListAPIView):
    permission_classes = (ReadOnly | (IsConsumer),)
    serializer_class = StoreListSerializer

    def get_queryset(self):
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

class CityStoreList(generics.ListAPIView):
    permission_classes = (ReadOnly | (IsConsumer),)
    serializer_class = StoreListSerializer

    def get_queryset(self):
        city_name = self.kwargs['city']
        city = get_object_or_404(City, name__iexact=city_name)
        try:
            vehicle_model = self.request.query_params.get('vehicle')
            vehicle_type = get_object_or_404(VehicleType, vehicle_model = vehicle_model)
            queryset = vehicle_type.stores.filter(city=city)
        except:
            queryset = city.stores.all()
        return queryset
from rest_framework import generics, status, filters, response
from common.permissions import *

from store.models import *
from store.serializers.general import *
import haversine as hs
from haversine import Unit
from django.shortcuts import get_object_or_404
from common.models import ServiceTag
from rest_framework.exceptions import NotFound
from geopy.geocoders import Nominatim, Photon
from rest_framework.response import Response
from store.serializers.services import *
import json


class StoreDetail(generics.RetrieveAPIView):
    lookup_field = 'slug'
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.filter(is_active=True)
    
    def get_object(self):
        instance = super().get_object()

        # subscribe to store topic
        user = self.request.user
        if user and user.is_active:
            user.sub_to_topic(user.id, instance.slug)
        

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
    
    def list(self, request, *args, **kwargs):
        response = super(CityStoreList, self).list(request, args, kwargs)
        response.data['results'] = sorted(response.data['results'], key=lambda k: (k['distance'], ))
        return response

    def get_queryset(self):
        citycode = self.kwargs['citycode']
        city = get_object_or_404(City, code__iexact=citycode)

        # subscribe user to city topic
        user = self.request.user
        if user and user.is_active:
            user.sub_to_topic(user.id, city.code)

        queryset = city.stores.filter(is_active=True)

        tag = self.request.GET.get('tag', None)

        if tag:
            tag = get_object_or_404(ServiceTag, slug=tag)
            services = Service.objects.filter(tags__in=[tag])
            price_times = PriceTime.objects.filter(store__in=queryset, service__in=services)
            return [ Store.objects.get(pk=store_id) for store_id in price_times.values_list('store', flat=True).distinct() ]

        return queryset

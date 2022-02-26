from rest_framework import generics, status, filters, response
from common.permissions import *

from store.models import *
from store.serializers.general import *
import haversine as hs
from haversine import Unit
from django.shortcuts import get_object_or_404
from django.db.models import F, Sum
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
    
    # def list(self, request, *args, **kwargs):
    #     response = super(CityStoreList, self).list(request, args, kwargs)
    #     response.data['results'] = sorted(response.data['results'], key=lambda k: ( float(k['distance'].strip('km').strip()), ))
    #     return response

    def get_queryset(self):
        citycode = self.kwargs['citycode']
        city = get_object_or_404(City, code__iexact=citycode)

        # subscribe user to city topic
        user = self.request.user
        if user and user.is_active:
            user.sub_to_topic(user.id, city.code)

        queryset = city.stores.filter(is_active=True).prefetch_related('pricetimes')
        
        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        search = self.request.query_params.get('search', None)
        tag = self.request.query_params.get('tag', None)
        sort = self.request.query_params.get('sort', None)
        
        # Use in case suryansh cries that search results should also be filtered by distance
        # if latitude and longitude:
        #     queryset = sorted( queryset, key=lambda store: ( store.get_distance(latitude, longitude), ) )
        #     queryset = city.stores.filter(pk__in=[ store.pk for store in queryset ])
        
        if latitude and longitude and not search and not tag:
            queryset = sorted( queryset, key=lambda store: ( store.get_distance(latitude, longitude), ) )

        if tag:
            tag = get_object_or_404(ServiceTag, slug=tag)
            services = Service.objects.filter(tags__in=[tag])
            price_times = PriceTime.objects.filter(store__in=queryset, service__in=services)
            store_list = [ Store.objects.get(pk=store_id) for store_id in price_times.values_list('store', flat=True).distinct() ]
            if sort:
                print('processing sorting: ', sort)
                if sort == 'price_lth':
                    return sorted( store_list, key=lambda store: ( 
                        store.pricetimes.filter(vehicle_type__wheel__code__icontains='four', is_offer=False).aggregate(Sum('price'))['price__sum'], 
                    ), reverse=True)
                elif sort == 'price_htl':
                    return sorted( store_list, key=lambda store: ( 
                        store.pricetimes.filter(vehicle_type__wheel__code__icontains='four', is_offer=False).aggregate(Sum('price'))['price__sum'], 
                    ), reverse=False)
            return sorted( store_list, key=lambda store: ( store.get_distance(latitude, longitude), ) )

        return queryset

from store.constants import VEHICLE_TYPES
from cart import serializer
from common.mixins import ValidateSerializerMixin
from vehicle.serializers import VehicleTypeSerializer
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ['question_text']
    

    def get_queryset(self):
        citycode = self.kwargs['citycode']
        city = get_object_or_404(City, code__iexact=citycode)
        queryset = city.stores.all()
        # if self.request.query_params.get('vehicle_model'):
        #     vehicle_model = self.request.query_params.get('vehicle_model')
        #     vehicle_type = get_object_or_404(VehicleType, model = vehicle_model)
        #     queryset = queryset.filter(supported_vehicle_types__in=[vehicle_type])
        return queryset

class StoreCreateView(generics.CreateAPIView, ValidateSerializerMixin):
    permission_classes = (IsSalesman,)   
    serializer_class = StoreCreateSerializer
    
    # def post(self, request, *args, **kwargs):

    #     data = self.validate(request)
    #     serializedData = self.get_serializer(data=data)
    #     serializedData.save()
        
    #     return response.Response({
    #         'message': 'Created Store'
    #     },status=status.HTTP_200_OK)

class ServiceCreationDetails(generics.GenericAPIView):
    # permission_classes = (IsSalesman | is)   
    # serializer_class = ServiceCreationDetailsSerializer
    

    def get(self, request):
        vehicle_types = VehicleTypeSerializer(VehicleType.objects.all(),many=True) 
        wheel_types = VEHICLE_TYPES
        services = ServiceSerializer(Service.objects.all(),many=True)
    
        return response.Response({
            'wheel_types': wheel_types,
            'vehicle_types': vehicle_types.data,
            'services' : services.data
        },status=status.HTTP_200_OK)        

class CreateStorePriceTimes(generics.GenericAPIView, ValidateSerializerMixin):
    permission_classes = (IsSalesman,)   
    serializer_class = CreatePriceTimeSerializer
    

    def post(self, request, *args, **kwargs):
        data = self.validate(request)
        serializer = CreatePriceTimeSerializer(data= data,many=True)
        serializer.save()
        return response.Response({
            "detail": "PriceTimes created" 
        }, status=status.HTTP_200_OK)


class StorePriceTimeList(generics.GenericAPIView, ValidateSerializerMixin):
    permission_classes = (IsSalesman,)   
    # serializer_class = StoreServiceListSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return self.request.user.salesman.stores.all()
    

    def get(self, request, slug):
        # TODO: send pricetime description too
        store = self.get_object()
        pricetimes = store.pricetimes.all()
        services = []
        store_price_times = {}
        for pricetime in pricetimes:
            service = pricetime.service
            if not  service in services:
                services.append(service)
        for service in services:
            store_price_times[service.id] = {'max_price':0,'min_price':float("inf"), 'max_slot_length':0,'min_slot_length':float("inf")}
        for pricetime in pricetimes:
            price = pricetime.price
            slot_length = pricetime.time_interval
            max_price = store_price_times[pricetime.service.id]['max_price']
            min_price = store_price_times[pricetime.service.id]['min_price']
            min_slot_length = store_price_times[pricetime.service.id]['min_slot_length']
            max_slot_length = store_price_times[pricetime.service.id]['max_slot_length']
            
            if slot_length > max_slot_length:
                store_price_times[pricetime.service.id]['max_slot_length'] = slot_length
            if slot_length < min_slot_length:
                store_price_times[pricetime.service.id]['min_slot_length'] = slot_length    
            if price > max_price:
                store_price_times[pricetime.service.id]['max_price'] = price
            if price < min_price:
                store_price_times[pricetime.service.id]['min_price'] = price    
        res = []
        for key in store_price_times:
            service = {}
            service['service']=ServiceSerializer(Service.objects.get(id=key)).data
            service['max_price']=store_price_times[key]['max_price']
            service['min_price']=store_price_times[key]['min_price']
            service['min_slot_length']=store_price_times[key]['min_slot_length']
            service['max_slot_length']=store_price_times[key]['max_slot_length']
            res.append(service)
#Yahan pe serializer use krna tha but samajh nahi aaya kese
        return response.Response(res, status=status.HTTP_200_OK)
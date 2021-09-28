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
from common.communication_provider import *


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
            user.sub_to_topic(instance.slug)
        

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
        if user and user.is_active:
            user.sub_to_topic(city.code)

        queryset = city.stores.filter(is_active=True)
        return queryset 

class StoreRegistrationEmail(generics.GenericAPIView):
    permission_classes = (IsSalesman,)
    lookup_field = 'slug'

    def get_queryset(self):
        return self.request.user.salesman.stores.all()

    def get(self, request, slug):
        store = self.get_object()
        if store.email is not None:
            email = store.email
            subject = "Subject"
            html_content = "<div>Hello <b>" + store.name +"</b></div>"
            cp = CommunicationProvider()
            cp.send_email(email, subject, html_content)
            return response.Response({
                "sent": True
            })
        else:
            return response.Response('Email Not Found.')

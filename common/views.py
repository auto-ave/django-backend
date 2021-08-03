from rest_framework import generics, response

from common.models import *
from common.serializers import *

class CityList(generics.GenericAPIView):
    
    def get(self, request, format=None):
        cities = City.objects.all()
        upcomings = City.objects.filter(upcoming=True)

        city_serializer = CitySerializer(cities, many=True)
        upcoming_serializer = CitySerializer(upcomings, many=True)

        return response.Response({
            'cities': city_serializer.data,
            'upcomings': upcoming_serializer.data
        })

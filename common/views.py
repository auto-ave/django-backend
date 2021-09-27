from rest_framework import generics, response, filters

from common.models import *
from common.serializers import *
from common.mixins import ValidateSerializerMixin

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

class ServiceList(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class CouponVerify(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = CouponVerifySerializer

    def post(self, request):
        data = self.validate(request)
        coupon = Coupon.objects.filter(code=data['code']).first()
        if coupon:
            return response.Response({
                'success': True,
                'message': 'Coupon is valid'
            })
        else:
            return response.Response({
                'success': False,
                'message': 'Coupon is invalid'
            })
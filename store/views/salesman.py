from rest_framework import generics, response, status
from common.permissions import *
from store.models import *
from store.serializers.general import *
from store.constants import VEHICLE_TYPES
from store.serializers.services import *
from cart import serializer
from common.mixins import ValidateSerializerMixin
from vehicle.serializers import VehicleTypeSerializer

class SalesmanStoreList(generics.ListAPIView):
    serializer_class = SalesmanStoreListSerializer
    permission_classes = (IsSalesman, )

    def get_queryset(self):
        user = self.request.user
        return user.salesman.stores.all()

class StoreCreateView(generics.CreateAPIView, ValidateSerializerMixin):
    permission_classes = (IsSalesman,)   
    serializer_class = StoreCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            salesman=user.salesman,
        )
        serializer.save()
    
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
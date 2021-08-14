from django.shortcuts import get_object_or_404
from rest_framework import generics, response, status, views
from uritemplate.api import partial
from common.permissions import *
from store.models import *
from store.serializers.general import *
from store.constants import VEHICLE_TYPES
from store.serializers.services import *
from cart import serializer
from common.mixins import ValidateSerializerMixin
from vehicle.serializers import VehicleTypeSerializer

class SalesmanStoreRetrieve(generics.RetrieveAPIView):
    serializer_class = SalesmanStoreListSerializer
    permission_classes = (IsSalesman, )
    lookup_field = 'slug'
    
    def get_queryset(self):
        user = self.request.user
        return user.salesman.stores.all()

class SalesmanStoreServiceRetrieve(generics.GenericAPIView):
    serializer_class = PriceTimeSerializer

    def get(self, request, slug, pk):
        user = self.request.user
        store = get_object_or_404(Store, slug=slug)

        if store.salesman != user.salesman:
            return response.Response({
                'detail': 'You are not allowed to create price times for this store'
            },status=status.HTTP_403_FORBIDDEN)
        if store.is_locked_for_salesman:
            return response.Response({
                'detail': 'Store is locked for salesman'
            },status=status.HTTP_400_BAD_REQUEST)

        service = get_object_or_404(Service, pk=pk)

        vehicle_types = VehicleTypeSerializer(VehicleType.objects.all(),many=True).data
        for type in vehicle_types:
            try:
                vehicle_type = VehicleType.objects.get(model=type['model'])
                pricetime = store.pricetimes.all().get(vehicle_type=vehicle_type, service=service)
                print(pricetime)
                type['id'] = pricetime.id
                type['price'] = pricetime.price
                type['time_interval'] = pricetime.time_interval
            except Exception as e:
                print('nhi mila pricetime: ', e)
                pass
        price_times = []
        for item in store.pricetimes.filter(service=service):
            price_times.append({
                "id": item.id,
                "vehicle_type": VehicleTypeSerializer(item.vehicle_type).data,
                "time_interval": item.time_interval,
                "price": item.price
            })

        print(store.pricetimes, store.pricetimes.all().first())
        return response.Response({
            "service" : {
                "name": service.name,
                "pk": service.pk
            },
            "description": store.pricetimes.all().first() and store.pricetimes.all().first().description,
            "images": store.pricetimes.all().first() and store.pricetimes.all().first().images,
            "price_times": vehicle_types
        })
    
    def delete(self, request, slug, pk):
        store = get_object_or_404(Store, slug=slug)
        if store.salesman != request.user.salesman:
            return response.Response({
                'detail': 'You are not allowed to delete price times for this store'
            },status=status.HTTP_403_FORBIDDEN)
        if store.is_locked_for_salesman:
            return response.Response({
                'detail': 'Store is locked for salesman'
            },status=status.HTTP_400_BAD_REQUEST)
        pricetimes = store.pricetimes.filter(service=pk)
        pricetimes.delete()
        return response.Response({
            "detail": "PriceTimes deleted"
        })


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
    #         'detail': 'Created Store'
    #     },status=status.HTTP_200_OK)

class ServiceCreationDetails(generics.GenericAPIView):
    # permission_classes = (IsSalesman | is)   
    # serializer_class = ServiceCreationDetailsSerializer
    

    def get(self, request, slug):
        vehicle_types = VehicleTypeSerializer(VehicleType.objects.all(),many=True).data
        wheel_types = VEHICLE_TYPES

        all_services = ServiceSerializer(Service.objects.all(),many=True).data
        final_services = []
        store = Store.objects.get(slug=slug)
        for service in all_services:
            if not store.pricetimes.all().filter(service=service['id']):
                final_services.append(service)
    
        return response.Response({
            'wheel_types': wheel_types,
            'vehicle_types': vehicle_types,
            'services' : final_services
        },status=status.HTTP_200_OK)        

class CreateStorePriceTimes(views.APIView):
    permission_classes = (IsSalesman,)   
    # serializer_class = CreatePriceTimeSerializer
    

    def post(self, request, *args, **kwargs):
        # data = self.validate(request)
        data = request.data
        # print(data)

        if not data.get('service'):
            return response.Response({
                'detail': 'service is required'
            },status=status.HTTP_400_BAD_REQUEST)

        store = Store.objects.get(slug=data.get('storeslug'))
        # TODO: create better permissions
        if store.salesman != request.user.salesman:
            return response.Response({
                'detail': 'You are not allowed to create price times for this store'
            },status=status.HTTP_403_FORBIDDEN)
        if store.is_locked_for_salesman:
            return response.Response({
                'detail': 'Store is locked for salesman'
            },status=status.HTTP_400_BAD_REQUEST)

        service = Service.objects.get(pk=data.get('service'))

        for item in data.get('pricetime_data'):
            vehicle = VehicleType.objects.get(model=item.get('vehicle_type'))
            print(item.get('id'), item)
            price_time = {
                    'store': store.pk,
                    'service': service.pk,
                    'vehicle_type': vehicle.pk,
                    'price': int(item.get('price')),
                    'time_interval': int(item.get('time_interval')),
                    'images': item.get('images') or service.images, ### Add service's images if emtpy
                    'description': item.get('description') or service.description ### Add service's description if emtpy
                }
            if item.get('id'):
                pricetimeInstance = store.pricetimes.get(pk=item.get('id'))
                serializer = CreatePriceTimeSerializer(pricetimeInstance, data=price_time, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            else:
                serializer = CreatePriceTimeSerializer(data=price_time)
                serializer.is_valid(raise_exception=True)
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
            store_price_times[pricetime.service.id]['description'] = pricetime.description
            
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
            service['description']=store_price_times[key]['description']
            res.append(service)
#Yahan pe serializer use krna tha but samajh nahi aaya kese
        return response.Response(res, status=status.HTTP_200_OK)
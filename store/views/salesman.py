from accounts.models import StoreOwner
from vehicle.models import Wheel, VehicleType
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
from vehicle.serializers import VehicleTypeSerializer, WheelSerializer
from common.communication_provider import *
from django.template.loader import get_template

class SalesmanStoreRetrieve(generics.RetrieveAPIView):
    serializer_class = SalesmanStoreListSerializer
    permission_classes = (IsSalesman, )
    lookup_field = 'slug'
    
    def get_queryset(self):
        user = self.request.user
        return user.salesman.stores.all()

class SalesmanStoreServiceRetrieve(generics.GenericAPIView):
    serializer_class = SalesmanStoreServiceRetrieveSerializer
    permission_classes = (IsSalesman, )
    queryset = PriceTime.objects.all()
    

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
        
        final_price_times = []
        description = service.description
        images = service.images
        
        price_times = store.pricetimes.filter(service=service).prefetch_related('vehicle_type')
        vehicle_types = VehicleType.objects.prefetch_related('wheel').all()
        
        for type in vehicle_types:
            pricetime = list( filter(lambda item: item.vehicle_type == type, list(price_times)) )
            if len(pricetime):
                pricetime = pricetime[0]
                description = pricetime.description
                images = pricetime.images
                final_price_times.append({
                    **VehicleTypeSerializer(type).data,
                    "id": pricetime.id,
                    "mrp": pricetime.mrp,
                    "price": pricetime.price,
                    "time_interval": pricetime.time_interval,
                })
            else:
                final_price_times.append(VehicleTypeSerializer(type).data)

        return response.Response({
            "service" : {
                "name": service.name,
                "pk": service.pk
            },
            "description": description,
            "images": images,
            "price_times": final_price_times
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

class StoreCreateView(generics.CreateAPIView):
    permission_classes = (IsSalesman,)
    serializer_class = StoreCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            slug = self.perform_create(serializer)
        except Exception as e:
            return response.Response({
                'error': str(e)
            })
        return response.Response({
            "slug": slug,
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        data = serializer.validated_data
        bay_number = data['bay_number']
        
        user = self.request.user
        data['salesman'] = user.salesman
        data['is_active'] = False
        del data['bay_number']

        store = Store.objects.create(**data)
        
        owner_user = User.objects.create(
            username=store.slug,
            email=store.email
        )
        owner_user.set_password('Qwerty@123')
        owner_user.save()
        
        owner_profile = StoreOwner.objects.create(user=owner_user)
        
        store.owner = owner_profile
        store.save()
        
        for index in range(bay_number):
            bay = Bay.objects.create(store=store)
        
        return store.slug

class StoreUpdateView(generics.UpdateAPIView):
    permission_classes = (IsSalesman,)
    serializer_class = StoreUpdateSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        user = self.request.user
        return user.salesman.stores.all()

class ServiceCreationDetails(generics.GenericAPIView):
    permission_classes = (IsSalesman, ) 
    serializer_class = ServiceCreationDetailsSerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        return self.request.user.salesman.stores.all()
    

    def get(self, request, slug):

        all_services = Service.objects.all()
        final_services = []
        store = self.get_object()
        all_pricetimes = store.pricetimes.all().prefetch_related('service')
        for service in all_services:
            pricetimes = list( filter(lambda item: item.service == service.id, list(all_pricetimes)) )
            if not pricetimes:
                final_services.append(service)
        final_services = ServiceSerializer(final_services, many=True).data
        
        vehicle_types = VehicleTypeSerializer(VehicleType.objects.all().prefetch_related('wheel').order_by('position'),many=True).data
        wheel_types = WheelSerializer(Wheel.objects.all(), many=True).data
        
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
                'mrp': int(item.get('mrp') or item.get('price')),
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
    serializer_class = StorePriceTimeListSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return self.request.user.salesman.stores.all()
    

    def get(self, request, slug):
        store = self.get_object()
        pricetimes = store.pricetimes.all().prefetch_related('service')
        services = []
        store_price_times = {}
        for pricetime in pricetimes:
            service = pricetime.service
            if not  service in services:
                services.append(service)
        for service in services:
            store_price_times[service.id] = {
                'service': service,
                'max_price':0,
                'min_price':float("inf"),
                'max_slot_length':0,
                'min_slot_length':float("inf")
            }
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
            # service['service']=ServiceSerializer(Service.objects.get(id=key)).data
            service['service']=ServiceSerializer(store_price_times[key]['service']).data
            service['max_price']=store_price_times[key]['max_price']
            service['min_price']=store_price_times[key]['min_price']
            service['min_slot_length']=store_price_times[key]['min_slot_length']
            service['max_slot_length']=store_price_times[key]['max_slot_length']
            service['description']=store_price_times[key]['description']
            res.append(service)
#Yahan pe serializer use krna tha but samajh nahi aaya kese
        return response.Response(res, status=status.HTTP_200_OK)


class StoreRegistrationEmail(generics.GenericAPIView):
    permission_classes = (IsSalesman,)
    serializer_class = StoreRegistrationEmailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return self.request.user.salesman.stores.all()

    def get(self, request, slug):
        store = self.get_object()
        if store.email is not None:
            email = store.email
            subject = "Store Registration"

            html_template = get_template('store_registration.html')
            html_content = html_template.render({ 'storeName': store.name })

            cp = CommunicationProvider()
            cp.send_email(email, subject, html_content)
            return response.Response({
                "success": "Mail Sent Successfully."
            }, status=200)
        else:
            return response.Response({
                "error": 'Email Not Found.'
            }, status=400)
from common.mixins import ValidateSerializerMixin
from vehicle.serializers import *

from rest_framework import generics, filters, response, status
from vehicle.models import *
from vehicle.utils import *

import requests
from django.db.models import Prefetch


class VehicleTypeListView(generics.ListAPIView):
    serializer_class = VehicleTypeSerializer

    def get_queryset(self):
        return VehicleType.objects.all()

class WheelListView(generics.ListAPIView):
    serializer_class = WheelSerializer

    def get_queryset(self):
        return Wheel.objects.all()

class VehicleBrandsListView(generics.ListAPIView):
    serializer_class = VehicleBrandSerializer

    def get_queryset(self):
        wheel = self.request.query_params.get('wheel', None)
        queryset = VehicleBrand.objects.all().prefetch_related(
            Prefetch(
                'vehicle_models',
                queryset=VehicleModel.objects.prefetch_related(
                    Prefetch(
                        'vehicle_type',
                        queryset=VehicleType.objects.prefetch_related(
                            'wheel'
                        )
                    )
                )
            )
        )
        result = []
        for brand in queryset:
            for model in brand.vehicle_models.all():
                if model.vehicle_type.wheel.code == wheel:
                    result.append(brand)
                    break
        return result

class VehicleModelsListView(generics.ListAPIView):
    serializer_class = VehicleModelSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=brand__name', ]

    def get_queryset(self):
        brand = self.request.query_params.get('brand')
        if brand:
            return VehicleModel.objects.filter(brand__name__iexact=brand)
        else:
            return VehicleModel.objects.none()

class VehicleModelFromRegView(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = VehicleModelFromRegSerializer

    def post(self, request):
        self.validate(request)
        data = request.data
        
        reg_num = data.get('reg_num').upper()
            
        reg_data_instance = VehicleRegistrationData.objects.filter(reg_num=reg_num).first()
        if reg_data_instance:
            print('data for {} already exists, using existing data'.format(reg_num))
            vehicle_data = getDataFromMotorcheckResponse(reg_data_instance.data)
        else:
            print('data for {} does not exist, fetching from motorcheck'.format(reg_num))
            res = requests.get('https://beta.motorcheck.ie/vehicle/reg/{}/identity/vin?_username=autoave&_api_key=9b8609d89b357031982381d0515b1f4269508b06'.format(reg_num))
            VehicleRegistrationData.objects.create(reg_num=reg_num, data=res.text)
            vehicle_data = getDataFromMotorcheckResponse(res.text)
        print('vehicle Data: ', vehicle_data)
        
        if vehicle_data.get('name') == 'NO_VEHICLE_DATA':
            return response.Response({
                'detail': 'No vehicle data found for {}'.format(reg_num)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        vehicle_model = VehicleModel.objects.filter(model=vehicle_data['model']).first()
        if vehicle_model:
            vehicle_type = vehicle_model.vehicle_type
        else:
            wheel = Wheel.objects.get(code=getWheelTypeFromReg(reg_num))
            
            vehicle_brand, vehicle_brand_created = VehicleBrand.objects.get_or_create(name=vehicle_data['make'])
            if vehicle_brand_created:
                print('vehicle brand created: ', vehicle_brand)
                
            vehicle_type, vehicle_type_created = VehicleType.objects.get_or_create(
                model=getVehicleTypeFromBody(vehicle_data['body']), wheel=wheel
            )
            if vehicle_type_created:
                print('vehicle type created: ', vehicle_type)
                
            vehicle_model, vehicle_model_created = VehicleModel.objects.get_or_create(
                brand=vehicle_brand,
                model=vehicle_data['model'],
                vehicle_type=vehicle_type
            )
            if vehicle_model_created:
                print('vehicle model created: ', vehicle_model)

            
        return response.Response(
            VehicleModelSerializer(vehicle_model, context={'request': self.request}).data
        )
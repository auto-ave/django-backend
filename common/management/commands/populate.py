from django.core.management.base import BaseCommand
from booking.models import BookingStatus
from common.providers.data_population import DataPopulationProvider

from common.data_population.serializers import *
from vehicle.models import VehicleBrand, VehicleModel, Wheel, VehicleType
from common.models import Service, City, ServiceTag

import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        POPULATION_DATA = [
            # Vehicle Related
            (VehicleBrand, None, 'common/data_population/vehicle_brands.json'),
            (Wheel, None, 'common/data_population/vehicle_wheels.json'),
            (VehicleType, VehicleTypePopulationSerializer, 'common/data_population/vehicle_types.json'),
            (VehicleModel, VehicleModelPopulationSerializer, 'common/data_population/vehicle_models.json'),
        
            # Common
            (Service, None, 'common/data_population/common_services.json'),
            (ServiceTag, None, 'common/data_population/common_service_tags.json'),
            (City, None, 'common/data_population/common_cities.json'),
            
            # Booking
            (BookingStatus, None, 'common/data_population/booking_statuses.json'),
        ]

        for data in POPULATION_DATA:
            model = data[0]
            serializer = data[1]
            file_path = data[2]

            with open(file_path) as f:
                data = json.load(f)
                provider = DataPopulationProvider(model=model, data=data, serializer=serializer)
                provider.populate()
        
        
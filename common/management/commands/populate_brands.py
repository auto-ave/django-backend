from django.core.management.base import BaseCommand, CommandError
from common.providers.data_population import DataPopulationProvider
from vehicle.models import *
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('common/data_population/brands.json') as f:
            brands_data = json.load(f)
        
        provider = DataPopulationProvider(model=VehicleBrand, data=brands_data)
        provider.populate()
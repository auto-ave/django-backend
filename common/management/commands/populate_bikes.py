from django.core.management.base import BaseCommand, CommandError
from vehicle.models import *
import json

class Command(BaseCommand):
    def handle(self, *args, **options):

        bikes = []
        with open('miscellaneous/vehicles_data/bikes.json') as json_file:
            bikes = json.load(json_file)

        for bike in bikes:
            brand = bike["Brand"]
            type = bike["Category"]
            name = bike["Model"]
            image = bike["Thumbnail"]
            vehicle_brand = VehicleBrand.objects.get(name=brand)
            vehicle_type = VehicleType.objects.get(model=type)
            new_bike = VehicleModel.objects.create(
                brand=vehicle_brand,
                vehicle_type = vehicle_type,
                model = name,
                image = image)
            new_bike.save()

        self.stdout.write(self.style.SUCCESS('Successfully created bikes models.'))
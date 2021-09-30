from django.core.management.base import BaseCommand, CommandError
from vehicle.models import *
import json

class Command(BaseCommand):
    def handle(self, *args, **options):

        cars = []
        with open('miscellaneous/vehicles_data/cars.json') as json_file:
            cars = json.load(json_file)

        for car in cars:
            brand = car["Brand"]
            type = car["Type"]
            name = car["Car"]
            image = car["Thumbnail"]
            vehicle_brand = VehicleBrand.objects.get(name=brand)
            vehicle_type = VehicleType.objects.get(model=type)
            new_car = VehicleModel.objects.create(
                brand=vehicle_brand,
                vehicle_type = vehicle_type,
                model = name,
                image = image)
            new_car.save()

        self.stdout.write(self.style.SUCCESS('Successfully created car models.'))
from django.core.management.base import BaseCommand, CommandError
from vehicle.models import *
import json

class Command(BaseCommand):
    def handle(self, *args, **options):

        wheels = []
        with open('miscellaneous/vehicles_data/wheels.json') as json_file:
            wheels = json.load(json_file)

        for wheel in wheels:
            try:
                fields = wheel["fields"]
                wheel_type = Wheel.objects.create(
                    code=wheel["pk"],
                    name = fields["name"],
                    image = fields["image"]
                )
                wheel_type.save()
            except:
                print("Wheel type exists.")

        vehicle_types = []
        with open('miscellaneous/vehicles_data/vehicle_types.json') as json_file:
            vehicle_types = json.load(json_file)

        for vehicle_type in vehicle_types:
            try:
                fields = vehicle_type["fields"]
                wheel = Wheel.objects.get(code=fields["wheel"])
                new_vehicle_type = VehicleType.objects.create(
                    model= vehicle_type["pk"],
                    image = fields["image"],
                    wheel = wheel
                )
                new_vehicle_type.save()
            except:
                print("Vehicle type exists.")

        self.stdout.write(self.style.SUCCESS('Successfully created bikes models.'))
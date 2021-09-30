from django.core.management.base import BaseCommand, CommandError
from vehicle.models import *
import json

class Command(BaseCommand):
    def handle(self, *args, **options):


        brands = []
        with open('miscellaneous/vehicles_data/carsbrands.json') as json_file:
            brands = json.load(json_file)

        print(brands)

        for brand in brands:
            try:
                new_brand = VehicleBrand.objects.create(name=brand['name'])
                new_brand.image = brand['image']
                new_brand.save()
            except:
                print(brand['name'])

        self.stdout.write(self.style.SUCCESS('Successfully created brands'))
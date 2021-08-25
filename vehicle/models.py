from django.db import models
from common.models import Model

from vehicle.constants import VEHICLE_MODELS, VEHICLE_TYPES

class VehicleType(Model):
    model = models.CharField(max_length=50, primary_key=True, help_text='Bike, Scooty, Sedan, Hachback, SUV, Truck, Bada Wala Truck')
    wheel = models.CharField(max_length=50, help_text='Two Wheeler, Three Wheeler, Four Wheeler, Commercial')
    description = models.TextField(blank=True, null=True)
    image = models.URLField(default="https://d3to388m2zu1ph.cloudfront.net/media/questions/g916_1_1.png")

    def __str__(self):
        return '{} : {}'.format(self.wheel, self.model)
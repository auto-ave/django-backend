from django.db import models
from common.models import Model

from vehicle.constants import VEHICLE_MODELS, VEHICLE_TYPES

class VehicleType(Model):
    model = models.CharField(max_length=50, primary_key=True, help_text='Bike, Scooty, Sedan, Hachback, SUV, Truck, Bada Wala Truck')
    # wheel = models.CharField(max_length=50, help_text='Two Wheeler, Three Wheeler, Four Wheeler, Commercial')
    wheel = models.ForeignKey('Wheel', on_delete=models.CASCADE, related_name='vehicle_types', null=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(default="https://d3to388m2zu1ph.cloudfront.net/media/questions/g916_1_1.png")
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.model

class Wheel(Model):
    code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, help_text='Two Wheeler, Three Wheeler, Four Wheeler, Commercial')
    image = image = models.URLField(default="https://d3to388m2zu1ph.cloudfront.net/media/questions/g916_1_1.png")

    def __str__(self):
        return self.name

class VehicleBrand(Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(default="https://d3to388m2zu1ph.cloudfront.net/media/questions/g916_1_1.png")

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name',]),
        ]

class VehicleModel(Model):
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE, related_name='vehicle_models')
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, related_name="vehicle_models")
    model = models.CharField(max_length=50, primary_key=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(default="https://d3to388m2zu1ph.cloudfront.net/media/questions/g916_1_1.png")

    def __str__(self):
        return '{} : {}'.format(self.brand, self.model)
    
    class Meta:
        ordering = ['model']
        indexes = [
            models.Index(fields=['model',]),
        ]

class VehicleRegistrationData(Model):
    reg_num = models.CharField(max_length=50, primary_key=True)
    data = models.TextField(blank=True, null=True)
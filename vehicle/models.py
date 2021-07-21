from django.db import models
from common.models import Model

from vehicle.constants import VEHICLE_MODELS, VEHICLE_TYPES

class VehicleType(Model):
    wheel = models.CharField(max_length=50, choices=VEHICLE_TYPES)
    model = models.CharField(max_length=50, choices=VEHICLE_MODELS, unique=True)

    def __str__(self):
        return '{} : {}'.format(self.wheel, self.model)
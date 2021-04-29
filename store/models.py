from django.db import models
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import Partner
from common.models import Model
from .static import VEHICLE_MODELS, VEHICLE_TYPES
# Create your models here.

class VehicleType(Model):
    vehicle_type = models.CharField(max_length=30, choices=VEHICLE_TYPES)
    vehicle_model = models.CharField(max_length=30, choices=VEHICLE_MODELS)

    def __str__(self):
        return self.vehicle_type + ": " + self.vehicle_model

    def save(self, *args, **kwargs):
        if self.vehicle_type == "two" and self.vehicle_model[-3:] == "two":
            super(VehicleType, self).save(*args, **kwargs)
        elif self.vehicle_type == "four" and self.vehicle_model[-4:] == "four":
            super(VehicleType, self).save(*args, **kwargs)
class Store(Model):
    thumbnail = models.ImageField()
    is_active = models.BooleanField()
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    contact_numbers = ArrayField(base_field=PhoneNumberField())
    emails = ArrayField(base_field=models.EmailField())
    address = models.TextField()
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    store_registration_type = models.CharField(max_length=30)
    store_registration_number = models.CharField(max_length=20)
    owner = models.OneToOneField(Partner, on_delete = models.CASCADE)
    vehicles_allowed = models.ManyToManyField(VehicleType)  # Non-Controllable Field
    contact_person_name = models.CharField(max_length=30)
    contact_person_number = PhoneNumberField()
    contact_person_photo = models.ImageField(null=True, blank =True)
    store_opening_time = models.TimeField()
    store_closing_time = models.TimeField()

    def __str__(self):
        return self.name


class StoreImage(Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE, related_name="store_images")
    image = models.ImageField()
    def __str__(self):
        return "{}: Image #{}".format(self.store.name, self.pk)


class Bay(Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE)
    vehicle_type = models.ManyToManyField(VehicleType)
    #per_vehicle_time_interval = models.ManyToManyField(Time)

    def __str__(self):
        return "{}: Image {}".format(self.store.name, self.pk)


class Service(Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    vehicles_allowed = models.ManyToManyField(VehicleType)

    def __str__(self):
        return "Service: " + self.name


class PriceTime(Model):
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    time_interval = models.PositiveIntegerField()

    class Meta:
        unique_together = ('vehicle_type', 'service')

    def save(self, *args, **kwargs):
        if self.vehicle_type in self.service.vehicles_allowed:
            super(PriceTime, self).save(*args, **kwargs)

class Event(Model):
    is_blocking = models.BooleanField()
    bay = models.ForeignKey(Bay, on_delete= models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return self.event_type + " #" + self.pk



    
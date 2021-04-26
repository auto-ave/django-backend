from django.db import models
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import Partner
from common.models import Model
# Create your models here.

class VehicleType(Model):
    vehicle_type = models.CharField(max_length=30)
    vehicle_model = models.CharField(max_length=30)

    def __str__(self):
        return self.vehicle_type + ": " + self.vehicle_model
class Store(Model):
    thumbnail = models.ImageField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    contact_numbers = ArrayField(base_field=PhoneNumberField())
    email = models.EmailField()
    address = models.TextField()
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    store_registration_type = models.CharField(max_length=30)
    store_registration_number = models.CharField(max_length=20)
    owner = models.OneToOneField(Partner, on_delete = models.CASCADE)
    vehicles_allowed = models.ManyToManyField(VehicleType)  # Non-Controllable Field

    def __str__(self):
        return self.name


class StoreImage(Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE)
    image = models.ImageField()
    related
    def __str__(self):
        return "{}: Image #{}".format(self.store.name, self.pk)


class Bay(Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE)
    vehicle_type = models.ManyToManyField(Vehicle)
    #per_vehicle_time_interval = models.ManyToManyField(Time)

    def __str__(self):
        return "{}: Image {}".format(self.store.name, self.pk)


class ServiceType(Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    vehicles_allowed = models.ManyToManyField(VehicleType)

    def __str__(self):
        return "Service: " + self.name
    

class PriceTime(Model):
    vehicle_type = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    service = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    time_interval = models.PositiveIntegerField()
    bay = models.ManyToManyField(Bay)



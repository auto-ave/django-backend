from django.db import models
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import Partner
# Create your models here.

class Store(models.Model):
    thumbnail = models.ImageField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    contact_numbers = ArrayField(base_field=PhoneNumberField)
    email = models.EmailField()
    address = models.TextField()
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    store_registration_type = models.CharField(max_length=30)
    store_registration_number = models.CharField(max_length=20)
    owner = models.OneToOneField(Partner, on_delete = models.CASCADE)
    vehicles_allowed = ArrayField(base_field=models.ManyToManyField(Vehicle))


    def __str__(self):
        return self.name


class StoreImages(models.Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return "{}: Image #{}".format(self.store.name, self.pk)
    

class Bay(models.Model):
    store = models.OneToOneField(Store, on_delete= models.CASCADE)
    vehicle_type = models.ManyToManyField(VehicleTypes)
    per_vehicle_time_interval = ArrayField(base_field=models.ManyToManyField(TimeOfWash, blank=True))

    def __str__(self):
        return "{}: Image {}".format(self.store.name, self.pk)

class Vehicle(models.Model):
    vehicle_type = models.CharField(max_length=30)
    vehicle_model = models.CharField(max_length=30)

    def __str__(self):
        return self.vehicle_type + ": " + self.vehicle_model

class Services(models.Model):
    store = models.OneToOneField(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return "Service: " + self.name
    

class Prices(models.Model):
    vehicle_type = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

class TimeOfWash(models.Model):
    vehicle_type = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    service = models.OneToOneField(Service, on_delete=models.CASCADE)
    time_interval = models.PositiveIntegerField()


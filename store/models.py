from django.db import models
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import Partner
from common.utils import *
from common.models import Model
from django.core.exceptions import ValidationError
from django.db import transaction
from store.constants import VEHICLE_MODELS, VEHICLE_TYPES

class VehicleType(Model):
    wheel = models.CharField(max_length=50, choices=VEHICLE_TYPES)
    model = models.CharField(max_length=50, choices=VEHICLE_MODELS, unique=True)

    def __str__(self):
        return '{} : {}'.format(self.wheel, self.model)

    # def save(self, *args, **kwargs):
    #     if self.wheel == "two" and self.model[-3:] == "two":
    #         super(VehicleType, self).save(*args, **kwargs)
    #     elif self.wheel == "four" and self.model[-4:] == "four":
    #         super(VehicleType, self).save(*args, **kwargs)
    #     else:
    #         raise ValidationError("Please select correct vehicle type and vehicle model")


class City(Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

    def __str__(self):
        return '{} {}'.format(self.code, self.name)
    
class Store(Model):
    thumbnail = models.ImageField()
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, editable=False, null=True)
    description = models.TextField(max_length=300)
    contact_numbers = ArrayField(base_field=PhoneNumberField())
    emails = ArrayField(base_field=models.EmailField())
    address = models.TextField()
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    store_registration_type = models.CharField(max_length=30)
    store_registration_number = models.CharField(max_length=20)
    owner = models.OneToOneField(Partner, on_delete = models.CASCADE)
    contact_person_name = models.CharField(max_length=30)
    contact_person_number = PhoneNumberField()
    contact_person_photo = models.ImageField(null=True, blank =True)
    store_opening_time = models.TimeField()
    store_closing_time = models.TimeField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    city = models.ForeignKey(City, related_name="stores", on_delete=models.CASCADE)
    supported_vehicle_types = models.ManyToManyField(VehicleType, blank=True, related_name= "stores") # Non-Controllable Field

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(Store, self).save(*args, **kwargs)

class StoreImage(Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE, related_name="store_images")
    image = models.ImageField()
    def __str__(self):
        return "{}: Image #{}".format(self.store.name, self.pk)

class Bay(Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE)

    # Cannot interpret the need of this field
    supported_vehicle_types = models.ManyToManyField(VehicleType, blank=True) # Display field (not for validation), updated after everything gets saved

    def __str__(self):
        return "{}: {}".format(self.pk, self.store)

class Service(Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    supported_vehicle_types = models.ManyToManyField(VehicleType, blank=True, related_name="services") # Display field (not for validation), updated after everything gets saved

    def __str__(self):
        return self.name


class PriceTime(Model):
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, related_name="vehicles")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    time_interval = models.PositiveIntegerField()
    bays = models.ManyToManyField(Bay)
    class Meta:
        unique_together = ('vehicle_type', 'service')

    def __str__(self):
        return "{} | {}".format(self.service, self.vehicle_type)

    # @transaction.atomic
    # def save(self, *args, **kwargs):
    #     super(PriceTime, self).save(*args, **kwargs)
    #     print("save(): ", self.id, self.bays.all(), self.service)
    #     self.updateBays()
    #     self.updateService()
    
    # def updateBays(self):
    #     print("updateBays: ", self.id, self.bays.all(), self.service)
    #     pass

    # def updateService(self):
    #     print("updateService: ", self.id, self.bays.all(), self.service)
    #     pass

class Event(Model):
    is_blocking = models.BooleanField()
    bay = models.ForeignKey(Bay, on_delete= models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return "{} | {}=>{}".format(self.bay, self.start_datetime, self.end_datetime)

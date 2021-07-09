from django.db import models
from django.contrib.postgres.fields import ArrayField
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import Partner
from common.utils import *
from common.models import Model, City
from vehicle.models import VehicleType
from django.core.exceptions import ValidationError
from django.db import transaction

class Store(Model):
    thumbnail = models.ImageField()
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True)
    description = models.TextField(max_length=300)
    contact_numbers = ArrayField(base_field=PhoneNumberField())
    emails = ArrayField(base_field=models.EmailField())
    address = models.TextField()
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    registration_type = models.CharField(max_length=30)
    registration_number = models.CharField(max_length=20)
    owner = models.OneToOneField(Partner, on_delete = models.CASCADE)
    contact_person_name = models.CharField(max_length=30)
    contact_person_number = PhoneNumberField()
    contact_person_photo = models.ImageField(null=True, blank =True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    city = models.ForeignKey(City, related_name="stores", on_delete=models.CASCADE)
    supported_vehicle_types = models.ManyToManyField(VehicleType, blank=True, related_name= "stores") # Non-Controllable Field

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(Store, self).save(*args, **kwargs)
    
    def updateRating(self, rating, isRemove = False):
        count = self.reviews.all().count()

        if self.rating:
            if isRemove:
                newRating = removeFromAverage(self.rating, count, rating)
            else:
                newRating = addToAverage(self.rating, count, rating)
        else:
            newRating = rating
        
        self.rating = newRating or None
        self.save()
        




class Bay(Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE)

    # Cannot interpret the need of this field
    supported_vehicle_types = models.ManyToManyField(VehicleType, blank=True) # Display field (not for validation), updated after everything gets saved

    def __str__(self):
        return "{}: {}".format(self.pk, self.store)

class Service(Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return '{} : {}'.format(self.code, self.name)


class PriceTime(Model):
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, related_name="vehicles")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    time_interval = models.PositiveIntegerField() # Number of minutes
    bays = models.ManyToManyField(Bay)
    
    class Meta:
        unique_together = ('vehicle_type', 'service')

    def __str__(self):
        return "{} | {}".format(self.vehicle_type, self.service)

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

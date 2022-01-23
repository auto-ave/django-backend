from django.db import models
from custom_admin_arrayfield.models.fields import ArrayField
from django.db.models import JSONField
from phonenumber_field.modelfields import PhoneNumberField
from common.utils import *
from common.models import Model, City, Service
from vehicle.models import VehicleType
from django.core.exceptions import ValidationError
from django.db import transaction
from store.schema import STORE_TIMES_FIELD_SCHEMA
from store.validators import JSONSchemaValidator

class Store(Model):
    owner = models.OneToOneField('accounts.StoreOwner', on_delete=models.SET_NULL, blank=True, null=True)
    partner = models.ForeignKey('accounts.Partner', related_name="stores", on_delete=models.SET_NULL, blank=True, null=True)
    salesman = models.ForeignKey('accounts.Salesman', related_name="stores", on_delete=models.SET_NULL, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_verified_by_admin = models.BooleanField(default=False, verbose_name="Verified by admin")
    is_locked_for_salesman = models.BooleanField(default=False, verbose_name="Locked for salesmanm if True salesman cannot edit this")

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField(max_length=900)
    thumbnail = models.URLField() # should be square
    images = ArrayField(base_field=models.URLField(), null=True, blank=True)
    contact_numbers = ArrayField(base_field=PhoneNumberField())
    # emails = ArrayField(base_field=models.EmailField())
    address = models.TextField()
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    merchant_id = models.CharField(max_length=30, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    # registration_number = models.CharField(max_length=20)
    
    contact_person_name = models.CharField(max_length=30)
    contact_person_number = PhoneNumberField()
    contact_person_photo = models.ImageField(null=True, blank =True)
    
    # TODO: json schema validation, change slot api, also frontend validation
    # Starts from sunday
    store_times = ArrayField(base_field=JSONField(), help_text='{"closing_time": "18:00", "opening_time": "09:00"}',
        validators=[JSONSchemaValidator(limit_value=STORE_TIMES_FIELD_SCHEMA)])
    display_opening_closing_time = models.CharField(max_length=100, null=True, blank=True)
    display_days_open = models.CharField(max_length=100, null=True, blank=True)

    # time in minutes to check if total service time should make an intra day service
    intra_day_time = models.SmallIntegerField(default=360) 
    
    
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    city = models.ForeignKey(City, related_name="stores", on_delete=models.CASCADE)

    services = models.ManyToManyField(Service, related_name="stores", blank=True)
    supported_vehicle_types = models.ManyToManyField(VehicleType, blank=True, related_name= "stores") # Non-Controllable Field

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id and not self.owner:
            print('IMP IMP IMP: store has no owner')
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
    store = models.ForeignKey(Store, on_delete= models.CASCADE, related_name="bays")

    # Cannot interpret the need of this field
    supported_vehicle_types = models.ManyToManyField(VehicleType, blank=True) # Display field (not for validation), updated after everything gets saved

    def __str__(self):
        return "{}: {}".format(self.pk, self.store)


class PriceTime(Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE, related_name="pricetimes")
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE, related_name="pricetimes")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="pricetimes")
    price = models.PositiveIntegerField()
    time_interval = models.PositiveIntegerField() # Number of minutes

    # images and description is redundant data and will be same for all the price times of same service
    images = ArrayField(base_field=models.URLField(), null=True, blank=True)
    description = models.TextField() # same descp for each type of vehicle

    bays = models.ManyToManyField(Bay,  blank=True, help_text="BUG: Do no edit this field, if you want to change bays delete this instance and create another one")
    
    class Meta:
        unique_together = ('vehicle_type', 'service', 'store')

    def __str__(self):
        return "{} | {}".format(self.vehicle_type, self.service)
    
    def save(self, *args, **kwargs):
        super(PriceTime, self).save(*args, **kwargs)

class Event(Model):
    is_blocking = models.BooleanField()
    bay = models.ForeignKey(Bay, on_delete= models.CASCADE, related_name="events")
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return "{} | {}=>{}".format(self.bay, self.start_datetime, self.end_datetime)

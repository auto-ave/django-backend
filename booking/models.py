from django.db import models
from common.models import Model
from django.contrib.postgres.fields import ArrayField
from accounts.models import Consumer
from store.models import Store, PriceTime, Event, VehicleType
from .static import BOOKING_STATUS, PAYMENT_STATUS
from common.utils import otp_generator
import datetime
# Create your models here.


class Booking(Model):
    booking_id = models.CharField(max_length=8)
    booked_by = models.ForeignKey(Consumer, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    status = models.PositiveIntegerField(choices=BOOKING_STATUS)
    status_changed_time = models.DateTimeField(default=datetime.datetime.now)
    otp = models.CharField(max_length=4)
    price_time = models.ForeignKey(PriceTime, on_delete=models.PROTECT)
    event = models.OneToOneField(Event, on_delete=models.PROTECT)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.PROTECT) # why is this needed? - subodh
    is_refunded = models.BooleanField(default=False)
    # invoice (File Field: To be completed by subodh)

    def __str__(self):
        return "Booking: #" + self.booking_id

    def save(self):
        self.otp = otp_generator()
        super(Booking, self).save()
    


class Payment(Model):
    booking = models.OneToOneField(Booking, on_delete=models.PROTECT)
    payment_status = models.IntegerField()
    transaction_id = models.CharField(max_length=10)
    mode_of_payment = models.CharField(max_length=20)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return "#{} Payment".format(self.booking.booking_id)

class Refund(Model):
    refund_status = models.IntegerField(choices=PAYMENT_STATUS)
    # details = returned from payment gateway
    booking = models.OneToOneField(Booking, on_delete=models.PROTECT)

    def save(self):
        if self.refund_status == 2:
            self.booking.is_refunded=True
        super(Refund, self).save()
        
class Review(Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    booking = models.OneToOneField(Booking, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    is_only_rating = models.BooleanField(default=True)
    review_description = models.CharField(max_length=250, blank=True, null=True)
    images = ArrayField(base_field=models.ImageField(), blank= True, null=True)
    rating = models.FloatField()

    def __str__(self):
        return "Review #{}".format(self.pk)
from django.db import models
from common.models import Model
from accounts.models import Consumer
from store.models import Store, PriceTime, Event, VehicleType
# Create your models here.


class Booking(Model):
    booking_id = models.CharField(max_length=8)
    booked_by = models.ForeignKey(Consumer)
    store = models.ForeignKey(Store)
    status = models.IntegerField()
    otp = models.IntegerField()
    price_time = models.ForeignKey(PriceTime)
    event = models.ForeignKey(Event)
    vehicle_type = models.ForeignKey(VehicleType)
    # invoice (File Field: To be completed by subodh)

    def __str__(self):
        return "Booking: #" + self.booking_id
    


class Payment(Model):
    booking = models.OneToOneField(Booking)
    payment_status = models.IntegerField()
    transaction_id = models.CharField(max_length=10)
    mode_of_payment = models.CharField(max_length=20)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return "#{} Payment".format(self.booking.booking_id)

class Refund(Model):
    refund_status = models.IntegerField()
    # details = returned from payment gateway
    booking = models.OneToOneField(Booking)
    pass

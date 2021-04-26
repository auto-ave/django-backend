from django.db import models
from common.models import Model
from accounts.models import Consumer
from store.models import Store, PriceTime, Event, VehicleType
# Create your models here.


class Booking(Model):
    booking_id = models.CharField(max_length=8)
    booked_by = models.ForeignKey(Consumer, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    status = models.IntegerField()
    otp = models.IntegerField()
    price_time = models.ForeignKey(PriceTime, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.PROTECT)
    # invoice (File Field: To be completed by subodh)

    def __str__(self):
        return "Booking: #" + self.booking_id
    


class Payment(Model):
    booking = models.OneToOneField(Booking, on_delete=models.PROTECT)
    payment_status = models.IntegerField()
    transaction_id = models.CharField(max_length=10)
    mode_of_payment = models.CharField(max_length=20)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return "#{} Payment".format(self.booking.booking_id)

class Refund(Model):
    refund_status = models.IntegerField()
    # details = returned from payment gateway
    booking = models.OneToOneField(Booking, on_delete=models.PROTECT)
    pass

class Review(Model):
    user = models.ForeignKey(Consumer, on_delete=models.PROTECT)
    booking = models.OneToOneField(Booking, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    is_only_rating = models.BooleanField(default=True)
    review_description = models.TextField(max_length=250, blank=True, null=True)
    images = ArrayField(base_field=models.ImageField(), blank= True, null=True)
    created_at = models.DateTimeField()
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return "Review #{}".format(self.pk)
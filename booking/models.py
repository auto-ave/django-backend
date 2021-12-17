from misc.email_contents import EMAIL_CONSUMER_CANCELLATION_REQUEST_APPROVED
from misc.notification_contents import NOTIFICATION_CONSUMER_BOOKING_COMPLETE, NOTIFICATION_CONSUMER_CANCELLATION_REQUEST_APPROVED, NOTIFICATION_CONSUMER_SERVICE_UNATTENDED, NOTIFICATION_CONSUMER_SERVICE_STARTED, NOTIFICATION_CONSUMER_SERVICE_COMPLETED
from common.communication_provider import CommunicationProvider
from cart.models import Cart
from django.db import models
from common.models import Model
from django.contrib.postgres.fields import ArrayField
from accounts.models import Consumer
from store.models import Store, PriceTime, Event, VehicleType
from .static import PAYMENT_STATUS, BookingStatusSlug
from common.utils import otp_generator
import datetime
from background_task import background

class BookingStatus(Model):
    
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta():
        verbose_name_plural = "Booking Statuses"
        
    
    def __str__(self):
        return self.slug

BookingStatus.__doc__ = "sdfasfd"

class Booking(Model):
    booking_id = models.CharField(primary_key=True, max_length=50)
    booked_by = models.ForeignKey(Consumer, on_delete=models.PROTECT, related_name='bookings')
    amount = models.CharField(max_length=30, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='bookings')
    
    # Breaking change
    booking_status = models.ForeignKey(BookingStatus, on_delete=models.PROTECT, related_name='bookings')
    
    booking_status_changed_time = models.DateTimeField(default=datetime.datetime.now)
    otp = models.CharField(max_length=4)
    price_times = models.ManyToManyField(PriceTime, related_name='bookings')
    event = models.OneToOneField(Event, on_delete=models.PROTECT, null=True, blank=True)
    vehicle_model = models.ForeignKey('vehicle.VehicleModel', on_delete=models.PROTECT, related_name='bookings', null=True)
    is_refunded = models.BooleanField(default=False)
    # invoice (File Field: To be completed by subodh)

    def __str__(self):
        return "Booking: #" + self.booking_id

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = otp_generator()
        super(Booking, self).save(*args, **kwargs)
    
    def start_service(self):
        self.booking_status = BookingStatus.objects.get(BookingStatusSlug.SERVICE_STARTED)
        self.booking_status_changed_time = datetime.datetime.now()
        self.save()
        # Service start notification
        CommunicationProvider.send_notification(
            **NOTIFICATION_CONSUMER_SERVICE_STARTED(self),
        )
    
    def complete_service(self):
        self.booking_status = BookingStatus.objects.get(BookingStatusSlug.SERVICE_COMPLETED)
        self.booking_status_changed_time = datetime.datetime.now()
        self.save()
        # Service complete notification
        CommunicationProvider.send_notification(
            **NOTIFICATION_CONSUMER_SERVICE_COMPLETED(self),
        )

    @background(schedule=0)
    def booking_unattended_check(bookingid):
        # Cannot take self as an argument in background tasks, therefore used bookingid
        booking = Booking.objects.get(booking_id=bookingid)
        print('Starting booking unattended check: ', booking, booking.status)
        try:
            if booking.booking_status == BookingStatus.objects.get(BookingStatusSlug.PAYMENT_SUCCESS):
                booking.booking_status = BookingStatus.objects.get(BookingStatusSlug.NOT_ATTENDED)
                booking.booking_status_changed_time = datetime.datetime.now()
                CommunicationProvider.send_notification(
                    **NOTIFICATION_CONSUMER_SERVICE_UNATTENDED(booking),
                )
                booking.save()
                return True
            return False
        except Exception as e:
            print("Error at Booking unattended check: ", e)
    
    def approve_cancellation_request(self):
        print("Approving cancellation request")
        self.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.CANCELLATION_REQUEST_APPROVED)
        self.booking_status_changed_time = datetime.datetime.now()
        self.save()
        # Cancellation approved notification and email
        CommunicationProvider.send_notification(
            **NOTIFICATION_CONSUMER_CANCELLATION_REQUEST_APPROVED(self),
        )
        CommunicationProvider.send_email(
            **EMAIL_CONSUMER_CANCELLATION_REQUEST_APPROVED(self),
        )

class Payment(Model):
    booking = models.OneToOneField(Booking, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    mode_of_payment = models.CharField(max_length=100, null=True, blank=True)
    amount = models.CharField(max_length=30, null=True, blank=True)
    gateway_name = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    payment_mode = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "#{} Payment".format(self.booking.booking_id)


class PartialPayment(Model):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name='partial_payments')
    status = models.CharField(max_length=100, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    mode_of_payment = models.CharField(max_length=100, null=True, blank=True)
    amount = models.CharField(max_length=30, null=True, blank=True)
    gateway_name = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    payment_mode = models.CharField(max_length=100, null=True, blank=True)


class Refund(Model):
    refund_status = models.IntegerField(choices=PAYMENT_STATUS)
    # details = returned from payment gateway
    booking = models.OneToOneField(Booking, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if self.refund_status == 2:
            self.booking.is_refunded=True
        super(Refund, self).save(*args, **kwargs)
        
class Review(Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, related_name="reviews")
    booking = models.OneToOneField(Booking, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="reviews")
    is_only_rating = models.BooleanField(default=True)
    review_description = models.CharField(max_length=250, blank=True, null=True)
    images = ArrayField(base_field=models.ImageField(), blank= True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)

    def save(self, *args, **kwargs):
        if not self.id:
            self.store.updateRating(self.rating)
        super(Review, self).save(*args, **kwargs)

    def __str__(self):
        return "Review #{} : {}".format(self.pk, self.store)

class Slot(Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return "Slot #{}".format(self.id)

class CancellationRequest(Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="cancellation_requests")
    reason = models.TextField()
    cancellation_status = models.TextField(help_text="To be filled by an Admin", blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.booking.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.CANCELLATION_REQUEST_SUBMITTED)
            self.booking.booking_status_changed_time = datetime.datetime.now()
            self.booking.save()
        super(CancellationRequest, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return "{} - {}".format(self.booking, self.reason)
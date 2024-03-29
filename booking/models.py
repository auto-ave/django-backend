# pylint: disable=no-member
from misc.email_contents import EMAIL_CONSUMER_CANCELLATION_REQUEST_APPROVED
from misc.notification_contents import NOTIFICATION_CONSUMER_CANCELLATION_REQUEST_APPROVED, NOTIFICATION_CONSUMER_CANCELLATION_REQUEST_RECIEVED, NOTIFICATION_CONSUMER_SERVICE_UNATTENDED, NOTIFICATION_CONSUMER_SERVICE_STARTED, NOTIFICATION_CONSUMER_SERVICE_COMPLETED
from common.communication_provider import CommunicationProvider
from django.db import models
from common.models import Model, Service
from django.contrib.postgres.fields import ArrayField
from misc.sms_contents import SMS_CONSUMER_CANCELLATION_APPROVED, SMS_CONSUMER_CANCELLATION_REQUESTED, SMS_CONSUMER_SERVICE_COMPLETE, SMS_CONSUMER_SERVICE_STARTED, SMS_CONSUMER_SERVICE_UNATTENDED
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

class Booking(Model):
    booking_id = models.CharField(primary_key=True, max_length=50)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    booked_by = models.ForeignKey('accounts.Consumer', on_delete=models.PROTECT, related_name='bookings')
    amount = models.CharField(max_length=30, null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='bookings')
    
    # Breaking change
    booking_status = models.ForeignKey(BookingStatus, on_delete=models.PROTECT, related_name='bookings')
    booking_status_changed_time = models.DateTimeField(default=datetime.datetime.now)
    
    offer = models.ForeignKey('booking.Offer', on_delete=models.SET_NULL, related_name="bookings", null=True, blank=True)
    
    otp = models.CharField(max_length=4)
    price_times = models.ManyToManyField(PriceTime, related_name='bookings')
    is_multi_day = models.BooleanField(default=False)
    event = models.OneToOneField(Event, on_delete=models.PROTECT, null=True, blank=True)
    vehicle_model = models.ForeignKey('vehicle.VehicleModel', on_delete=models.PROTECT, related_name='bookings', null=True)
    # invoice (File Field: To be completed by subodh)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['razorpay_order_id']),
        ]
    
    def __str__(self):
        return "Booking: #" + self.booking_id

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = otp_generator()
        super(Booking, self).save(*args, **kwargs)
    
    def has_payment(self):
        if hasattr(self, 'payment'):
            return True
        else:
            return False
    
    def get_booking_status_display(self):
        return self.booking_status.slug
    
    def start_service(self):
        self.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.SERVICE_STARTED)
        self.booking_status_changed_time = datetime.datetime.now()
        self.save()
        # Service start notification
        CommunicationProvider.send_notification(
            **NOTIFICATION_CONSUMER_SERVICE_STARTED(self),
        )
        CommunicationProvider.send_sms(
            **SMS_CONSUMER_SERVICE_STARTED(self)
        )
    
    def complete_service(self):
        self.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.SERVICE_COMPLETED)
        self.booking_status_changed_time = datetime.datetime.now()
        self.save()
        # Service complete notification
        CommunicationProvider.send_notification(
            **NOTIFICATION_CONSUMER_SERVICE_COMPLETED(self),
        )
        CommunicationProvider.send_sms(
            **SMS_CONSUMER_SERVICE_COMPLETE(self)
        )
        

    @background(schedule=0)
    def booking_unattended_check(bookingid):
        # Cannot take self as an argument in background tasks, therefore used bookingid
        booking = Booking.objects.get(booking_id=bookingid)
        try:
            if booking.booking_status == BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_SUCCESS):
                booking.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.NOT_ATTENDED)
                booking.booking_status_changed_time = datetime.datetime.now()
                CommunicationProvider.send_notification(
                    **NOTIFICATION_CONSUMER_SERVICE_UNATTENDED(booking),
                )
                CommunicationProvider.send_sms(
                    **SMS_CONSUMER_SERVICE_UNATTENDED(booking),
                )
                booking.save()
                return True
            return False
        except Exception as e:
            print("Error at Booking unattended check: ", e)
    
    def submit_cancellation_request(self):
        print("Submitting cancellation request")
        self.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.CANCELLATION_REQUEST_SUBMITTED)
        self.booking_status_changed_time = datetime.datetime.now()
        self.save()
        # Cancellation approved notification and email
        CommunicationProvider.send_notification(
            **NOTIFICATION_CONSUMER_CANCELLATION_REQUEST_RECIEVED(self),
        )
        CommunicationProvider.send_sms(
            **SMS_CONSUMER_CANCELLATION_REQUESTED(self),
        )
   
    def approve_cancellation_request(self):
        print("Approving cancellation request")
        if self.booking_status == BookingStatus.objects.get(slug=BookingStatusSlug.CANCELLATION_REQUEST_SUBMITTED):
            self.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.CANCELLATION_REQUEST_APPROVED)
            self.booking_status_changed_time = datetime.datetime.now()
            self.save()
            # Cancellation approved notification and email
            CommunicationProvider.send_notification(
                **NOTIFICATION_CONSUMER_CANCELLATION_REQUEST_APPROVED(self),
            )
            CommunicationProvider.send_sms(
                **SMS_CONSUMER_CANCELLATION_APPROVED(self),
            )
            if self.booked_by.user.email:
                CommunicationProvider.send_email(
                    **EMAIL_CONSUMER_CANCELLATION_REQUEST_APPROVED(self),
                )
        else:
            print('already approved cancellation request for {} this booking'.format(self.booking_id))

class Payment(Model):
    booking = models.OneToOneField(Booking, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    mode_of_payment = models.CharField(max_length=100, null=True, blank=True)
    amount = models.CharField(max_length=30, null=True, blank=True)
    gateway_name = models.CharField(max_length=100, null=True, blank=True)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    payment_mode = models.CharField(max_length=100, null=True, blank=True)
    rp_signature = models.CharField(max_length=200, null=True, blank=True)
    
    created_by_webhook = models.BooleanField(default=False)

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
    consumer = models.ForeignKey('accounts.Consumer', on_delete=models.CASCADE, related_name="reviews")
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


class CancellationRequest(Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="cancellation_requests")
    reason = models.TextField()
    cancellation_status = models.TextField(help_text="To be filled by an Admin", blank=True, null=True)
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="approved_cancellation_requests", blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.booking.submit_cancellation_request()
        super(CancellationRequest, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return "{} - {}".format(self.booking, self.reason)


class ActiveOfferManager(models.Manager):
    def active_offers(self):
        return super().get_queryset().all()

class Offer(Model):
    code = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    banner = models.ImageField(upload_to='offer_banners', null=True, blank=True)
    is_promo = models.BooleanField(default=False)
    
    # Greater the priority, higher the offer comes in a list
    priority = models.IntegerField(default=1)
    
    discount_percentage = models.IntegerField(default=10)
    max_discount = models.IntegerField(default=0)
    
    min_booking_amount = models.IntegerField(default=0)
    max_booking_amount = models.IntegerField(default=0)
    
    linked_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="offers", null=True, blank=True)
    applicable_services = models.ManyToManyField(Service, related_name="applicable_on_offers", blank=True) # if len more than 0 -> offer applicable on these services only
    services_to_add = models.ManyToManyField(Service, related_name="will_be_added_on_offers", blank=True) # these services will be added to cart on applying this offer
    
    max_redeem_count = models.IntegerField(default=10, help_text="Maximum number of times a offer can be used in total, 0 for unlimited")
    max_redeem_count_per_cosumer = models.IntegerField(default=2, help_text="Maximum number of times a offer can be used by one user, 0 for unlimited")
    
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    
    objects = ActiveOfferManager()

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super(Offer, self).save(*args, **kwargs)
    
    def is_valid(self):
        if not self.is_active:
            return False
        if self.valid_from and self.valid_to:
            if self.valid_from > datetime.datetime.now() or self.valid_to < datetime.datetime.now():
                return False
        return True

    def get_discount_amount_from_sub_total(self, subtotal):
        offer = self
        subtotal = float(subtotal)
        
        discount_percentage = offer.discount_percentage / 100 # since we store in percentage
        max_discount = offer.max_discount
        
        raw_discount = round(subtotal * discount_percentage, 2)
        if raw_discount > max_discount:
            raw_discount = max_discount
        
        return raw_discount

    def __str__(self):
        return '{} - {}'.format(self.code, self.title)

class OfferRedeem(Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="redeems")
    consumer = models.ForeignKey('accounts.Consumer', on_delete=models.CASCADE, related_name="redeems")
    
    def __str__(self) -> str:
        return "{} - {}".format(self.offer, self.consumer)
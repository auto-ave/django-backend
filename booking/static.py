from django.apps import apps


####
#### MASTER DATA CONTAINING ALL THE BOOKING STATUS VALUES
#### THIS DATA SHOULD BE INSYNC WITH THE common/data_population/booking_status.py file
####
class BookingStatusSlug():
    INITIATED = 'INITIATED'
    PAYMENT_FAILED = 'PAYMENT_FAILED'
    PAYMENT_SUCCESS = 'PAYMENT_SUCCESS'
    NOT_ATTENDED = 'NOT_ATTENDED'
    SERVICE_STARTED = 'SERVICE_STARTED'
    SERVICE_COMPLETED = 'SERVICE_COMPLETED'
    CANCELLATION_REQUEST_SUBMITTED = 'CANCELLATION_REQUEST_SUBMITTED'
    CANCELLATION_REQUEST_APPROVED = 'CANCELLATION_REQUEST_APPROVED'
    CANCELLATION_REQUEST_REJECTED = 'CANCELLATION_REQUEST_REJECTED'


PAYMENT_STATUS = (
    (0, 'Pending'),
    (1, 'Paid'),
    (2, 'Cancelled')
)
PAYMENT_STATUS_DICT = dict((v, k) for k, v in PAYMENT_STATUS)


# Max length per reason limit to 500
BOOKING_CANCEL_REASONS = [
    "Want to book another time slot",
    "I am not available for the service",
]

BOOKING_CANCEL_PRIOR_HOURS = 12

class RazorpayWebhookEvents():
    PAYMENT_CAPTURED = 'payment.captured'
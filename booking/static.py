BOOKING_STATUS = (
    (0, 'Not Paid'),
    (10, 'Payment Done'),
    (20, 'Payment Failed'),
    (30, 'Not Attended'),
    (40, 'Service Started'),
    (50, 'Service Completed')
)
BOOKING_STATUS_DICT = dict((v, k) for k, v in BOOKING_STATUS)

PAYMENT_STATUS = (
    (0, 'Pending'),
    (1, 'Paid'),
    (2, 'Cancelled')
)
PAYMENT_STATUS_DICT = dict((v, k) for k, v in PAYMENT_STATUS)
BOOKING_STATUS = (
    (0, 'Not Paid'),
    (1, 'Payment Done'),
    (2, 'Not Attended'),
    (3, 'Service Started'),
    (4, 'Service Completed'),
    (5, 'Cancelled')
)
BOOKING_STATUS_DICT = dict((v, k) for k, v in BOOKING_STATUS)

PAYMENT_STATUS = (
    (0, 'Pending'),
    (1, 'Paid'),
    (2, 'Cancelled')
)
PAYMENT_STATUS_DICT = dict((v, k) for k, v in PAYMENT_STATUS)
import enum

BOOKING_STATUS = (
    (0, 'NOT_PAID'),
    (10, 'PAYMENT_DONE'),
    (20, 'PAYMENT_FAILED'),
    (30, 'NOT_ATTENDED'),
    (40, 'SERVICE_STARTED'),
    (50, 'SERVICE_COMPLETED')
)
BOOKING_STATUS_DICT = dict((v, k) for k, v in BOOKING_STATUS)
BOOKING_STATUS_DICT = enum.IntEnum('BOOKING_STATUS_DICT', BOOKING_STATUS_DICT)

PAYMENT_STATUS = (
    (0, 'Pending'),
    (1, 'Paid'),
    (2, 'Cancelled')
)
PAYMENT_STATUS_DICT = dict((v, k) for k, v in PAYMENT_STATUS)
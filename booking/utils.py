import uuid
from .models import BookingStatus
from booking.static import BookingStatusSlug
from booking.models import Booking

from django.db.models import Prefetch

from common.utils import DATETIME_TODAY_END, DATETIME_TODAY_START


####
#### Function to get Commission slabs
####
def get_commission_percentage(amount):
    amount = float(amount)
    if amount > 10000:
        return 0.10
    if amount > 1000:
        return 0.15
    return 0.20

def get_commission_amount(amount):
    amount = float(amount)
    return round(amount * get_commission_percentage(amount), 2)

def check_time_range_overlap(start1, end1, start2, end2):
    if start1 >= start2 and start1 <= end2:
        return True
    if end1 >= start2 and end1 <= end2:
        return True
    if start1 <= start2 and end1 >= end2:
        return True
    return False

def check_event_collide_in_store(start, end, store):
    bays = store.bays.all()
    colliding_events = []
    booking_init_status = BookingStatus.objects.get(slug=BookingStatusSlug.INITIATED)
    count = 0
    for bay in bays:
        events = bay.events.prefetch_related(
            Prefetch( 'booking', queryset=Booking.objects.select_related('booking_status') )
        ).filter(
            start_datetime__gte=DATETIME_TODAY_START,
            end_datetime__lte=DATETIME_TODAY_END
        )
        for event in events:
            if hasattr(event, 'booking') and event.booking.booking_status == booking_init_status:
                continue
            if check_time_range_overlap(start, end, event.start_datetime, event.end_datetime):
                count = count + 1
                colliding_events.append(event)
                break
    if count == bays.count():
        return True
    return False


def generate_booking_id():
    return uuid.uuid4().hex[:10].upper()
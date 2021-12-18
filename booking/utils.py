import uuid


####
#### Function to get Commission slabs
####
def get_commission_percentage(amount):
    amount = float(amount)
    if amount > 5000:
        return 0.10
    if amount > 1000:
        return 0.15
    return 0.20

def get_amount_after_commission(amount):
    amount = float(amount)
    return float(amount) * (1 - get_commission_percentage(amount))


def check_event_collide(start, end, store):
    return False


def generate_booking_id():
    return uuid.uuid4().hex[:10].upper()
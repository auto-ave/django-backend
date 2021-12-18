
####
#### Function to get Commission slabs
####
def get_commission_percentage(amount):
    if amount > 5000:
        return 0.10
    if amount > 1000:
        return 0.15
    return 0.20


def check_event_collide(start, end, store):
    return False


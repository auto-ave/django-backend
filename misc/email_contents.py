from misc.contact_details import CONTACT_EMAIL


def EMAIL_CONSUMER_BOOKING_COMPLETE(booking):
    store = booking.store
    vehicle_model = booking.vehicle_model
    event = booking.event
    return {
        'email': booking.booked_by.user.email,
        'subject': 'Booking confirmed at {}'.format(store.name),
        'html_content': 'Your booking for {} {} on {} has been confirmed. Be sure to reach the store on time.'.format(vehicle_model.brand, vehicle_model.model, event.start_datetime.strftime('%d %b')),
        
    }

def EMAIL_CONSUMER_CANCELLATION_REQUEST_APPROVED(booking):
    return {
        'email': booking.booked_by.user.email,
        'subject': 'Cancellation Request Approved',
        'html_content': 'Your cancellation request for booking ID #{} has been approved. A refund of ₹{} has been initiated towards your original payment method. Feel free to contact us at {} if you have any queries.'.format(booking.booking_id, booking.amount, CONTACT_EMAIL), 
    }

# Created just for testing out emails
def EMAIL_CONSUMER_BOOKING_INITIATED(booking):
    store = booking.store
    vehicle_model = booking.vehicle_model
    event = booking.event
    return {
        'email': booking.booked_by.user.email,
        'subject': 'Booking initiated at {}'.format(store.name),
        'html_content': 'Your booking for {} {} on {} has been initiated.'.format(vehicle_model.brand, vehicle_model.model, event.start_datetime.strftime('%d %b')),
    }

def EMAIL_OWNER_BOOKING_COMPLETE(booking):
    store = booking.store
    vehicle_model = booking.vehicle_model
    event = booking.event
    return {
        'email': [store.owner.user.email, store.email],
        'subject': 'New booking on {} for {} {}'.format(event.start_datetime.strftime('%d %b - %I:%M %p'), vehicle_model.brand, vehicle_model.model),
        'html_content': 'Booking for {} {} on {} has been confirmed. Be sure to reach the store on time.'.format(vehicle_model.brand, vehicle_model.model, event.start_datetime.strftime('%d %b')),
        
    }
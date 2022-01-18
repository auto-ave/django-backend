from common.utils import dateTimeDiffInMinutes
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

def EMAIL_OWNER_NEW_BOOKING(booking):
    store = booking.store
    vehicle_model = booking.vehicle_model
    event = booking.event
    user = booking.booked_by.user
    return {
        "email": store.email,
        "subject": "New booking on {} for {} {}".format(event.start_datetime.strftime('%d %b - %I:%M %p'), vehicle_model.brand, vehicle_model.model),
        "html_content": "Booking for {} {} on {} has been confirmed.".format(vehicle_model.brand, vehicle_model.model, event.start_datetime.strftime('%d %b')),
        "template_id": "d-28d7bcd7d3854ec8ae3bf9b4aa2be5fd",
        "dynamic_template_data": {
            "booking_id": str(booking.booking_id),
            "store_name": str(store.name),
            "vehicle": {
                "brand": str(vehicle_model.brand.name),
                "model": str(vehicle_model.model),
            },
            "slot": {
                "start_time": event.start_datetime.strftime('%d %b - %I:%M %p'),
                "end_time": event.end_datetime.strftime('%d %b - %I:%M %p'),
                "duration": int(dateTimeDiffInMinutes(event.end_datetime, event.start_datetime)),
                "date": event.start_datetime.strftime('%d %b'),
            },
            "remaining_amount": float(booking.amount) - float(booking.payment.amount),
            "paid_amount": float(booking.payment.amount),
            "services": [ str(item.service.name) for item in booking.price_times.all() ],
            "customer": {
                "name": str(user.full_name()),
                "phone": str(user.phone),
                "email": str(user.email)
            }
        }
    }
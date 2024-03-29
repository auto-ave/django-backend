from common.utils import random_item, secondsToTimeString
from misc.contact_details import CONTACT_EMAIL


MODI_IMAGES = [
    'https://i.tribune.com.pk/media/images/1038308-MODI-1454343716/1038308-MODI-1454343716.jpg'
    'https://images.financialexpress.com/2018/05/modi-demonetsaition-gst.jpg',
    'https://www.deccanherald.com/sites/dh/files/styles/article_detail/public/article_images/2019/08/18/file76ocnj65hl4sm06z2bs-1566107661.jpg?itok=qhPn_u8r',
    'https://imgeng.jagran.com/images/2021/aug/independence-day-515974597096351628944205637.jpg',
    'https://www.indiatoday.in/india/wp-content/uploads/2019/08/modi-1.jpg',
    'https://static.toiimg.com/thumb/msid-71421766,width-1200,height-900,resizemode-4/.jpg',

]

def NOTIFICATION_CONSUMER_BOOKING_COMPLETE(booking):
    store = booking.store
    vehicle_model = booking.vehicle_model
    event = booking.event
    return {
        'title': 'Booking confirmed at {}'.format(store.name),
        'body': 'Your booking for {} {} on {} has been confirmed. Be sure to reach the store on time.'.format(
            vehicle_model.brand, 
            vehicle_model.model, 
            event.start_datetime.strftime('%d %b')
        ),
        'userid': booking.booked_by.user.id
    }

def NOTIFICATION_CONSUMER_BOOKING_CANCELLED(booking):
    store = booking.store
    vehicle_model = booking.vehicle_model
    event = booking.event
    return {
        'title': 'Booking cancelled at {}'.format(store.name),
        'body': 'Your booking for {} {} on {} has been cancelled. If you are not sure why this happened, feel free to contact us at {}'.format(vehicle_model.brand, vehicle_model.model, event.start_datetime.strftime('%d %b'), CONTACT_EMAIL),
        'userid': booking.booked_by.user.id
    }

def NOTIFICATION_CONSUMER_2_HOURS_LEFT(booking):
    store = booking.store
    return {
        'title': '2 Hours to go!',
        'body': 'Your booking at {} is in 2 hours. Hope to see you on time.'.format(store.name),
        'userid': booking.booked_by.user.id
    }

def NOTIFICATION_CONSUMER_SERVICE_STARTED(booking):
    store = booking.store
    event = booking.event
    seconds = (event.end_datetime - event.start_datetime).seconds
    return {
        'title': 'Your service at {} has been started'.format(store.name),
        'body': 'It will take around {} to get your vehicle ready. Thank you for your patience.'.format(secondsToTimeString(seconds)),
        'userid': booking.booked_by.user.id
    }

def NOTIFICATION_CONSUMER_SERVICE_COMPLETED(booking):
    store = booking.store
    return {
        'title': 'Your service at {} has been completed'.format(store.name),
        'body': 'Your vehicle is ready to be picked up. Hope you are happy with the services.',
        'userid': booking.booked_by.user.id
    }

def NOTIFICATION_CONSUMER_SERVICE_UNATTENDED(booking):
    store = booking.store
    return {
        'title': 'Service Missed'.format(store.name),
        'body': "You didn't appear for your booking at {}. We hope that everything is fine and you are in good health.".format(store.name),
        'userid': booking.booked_by.user.id
    }

def NOTIFICATION_CONSUMER_CANCELLATION_REQUEST_RECIEVED(booking):
    return {
        'title': 'Cancellation Request Submitted',
        'body': 'Your cancellation request for booking ID #{} has been recieved. Our team is currently reviewing your request and will revert back to you in 1-3 business days. Thank you for your patience.'.format(booking.booking_id),
        'userid': booking.booked_by.user.id
    }

def NOTIFICATION_CONSUMER_CANCELLATION_REQUEST_APPROVED(booking):
    return {
        'title': 'Cancellation Request Approved',
        'body': 'Your cancellation request for booking ID #{} has been approved. A refund of ₹{} has been initiated towards your original payment method. Feel free to contact us at {} if you have any queries.'.format(
            booking.booking_id,
            booking.payment.amount,
            CONTACT_EMAIL
        ),
        'userid': booking.booked_by.user.id
    }

def NOTIFICATION_OWNER_NEW_BOOKING(booking):
    store = booking.store
    vehicle_model = booking.vehicle_model
    event = booking.event
    return {
        'title': 'New booking on {} for {} {}'.format(event.start_datetime.strftime('%d %b - %I:%M %p'), vehicle_model.brand, vehicle_model.model),
        'body': 'Booking for {} {} on {} has been confirmed. Be sure to complete the service on time and collect the due amount displayed on your mobile application.'.format(
            vehicle_model.brand,
            vehicle_model.model,
            event.start_datetime.strftime('%d %b')
        ),
        'userid': store.owner.user.id,
        'data': {
            'reload': "true",
        }
    }

# Only created to test notifis
def NOTIFICATION_OWNER_BOOKING_INITIATED(booking):
    store = booking.store
    vehicle_model = booking.vehicle_model
    event = booking.event
    return {
        'title': 'Initiated booking on {} for {} {}'.format(event.start_datetime.strftime('%d %b - %I:%M %p'), vehicle_model.brand, vehicle_model.model),
        'body': 'Booking for {} {} on {} has been confirmed. # TODO: content'.format(vehicle_model.brand, vehicle_model.model, event.start_datetime.strftime('%d %b')),
        'userid': store.owner.user.id
    }

def NOTIFICATION_CUSTOMER_BOOKING_INITIATED(booking):
    store = booking.store
    vehicle_model = booking.vehicle_model
    event = booking.event
    return {
        'title': 'Initiated booking on {} for {} {}'.format(event.start_datetime.strftime('%d %b - %I:%M %p'), vehicle_model.brand, vehicle_model.model),
        'body': 'Booking for {} {} on {} has been initiated.'.format(vehicle_model.brand, vehicle_model.model, event.start_datetime.strftime('%d %b')),
        'userid': booking.booked_by.user.id
    }
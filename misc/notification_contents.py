from common.utils import secondsToTimeString
from misc.contact_details import CONTACT_EMAIL

def NOTIFICATION_BOOKING_COMPLETE(store, vehicle_type, event):
    return {
        'title': 'Booking confirmed at {}'.format(store.name),
        'body': 'Your booking for {} {} on {} has been confirmed. Be sure to reach the store on time.'.format(vehicle_type.wheel, vehicle_type.model, event.start_datetime.strftime('%d %b')),
        'image': 'https://i.tribune.com.pk/media/images/1038308-MODI-1454343716/1038308-MODI-1454343716.jpg'
    }

def NOTIFICATION_BOOKING_CANCELLED(store, vehicle_type, event):
    return {
        'title': 'Booking cancelled at {}'.format(store.name),
        'body': 'Your booking for {} {} on {} has been cancelled. If you are not sure why this happened, feel free to contact us at {}'.format(vehicle_type.wheel, vehicle_type.model, event.start_datetime.strftime('%d %b'), CONTACT_EMAIL),
        'image': ''
    }

def NOTIFICATION_SERVICE_STARTED(store, event):
    seconds = event.start_datetime - event.end_datetime
    return {
        'title': 'You service at {} has been started'.format(store.name),
        'body': 'It will take around {} to get your vehicle ready. Thank you for your patience.'.format(secondsToTimeString(seconds)),
        'image': ''
    }

def NOTIFICATION_SERVICE_COMPLETED(store):
    return {
        'title': 'You service at {} has been completed'.format(store.name),
        'body': 'Your vehicle is ready to be picked up. Hope you are happy with the services.',
        'image': ''
    }
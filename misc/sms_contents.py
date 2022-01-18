from common.utils import secondsToTimeString


def SMS_LOGIN_CONTENT(user):
    phone = user.phone_sms()
    return {
        'message_id': '135921',
        'variables_values': '{}|'.format(user.otp),
        'numbers': phone,
    }

def SMS_CONSUMER_BOOKING_COMPLETE(booking):
    store = booking.store
    vehicle_model = booking.vehicle_model
    event = booking.event
    phone = booking.booked_by.user.phone_sms()
    return {
        'message_id': '135924',
        'variables_values': '{}|{}|{}|{}|{}|'.format(
            vehicle_model.brand, 
            vehicle_model.model, 
            event.start_datetime.strftime('%d %b'),
            store.name,
            booking.otp
        ),
        'numbers': phone,
    }

def SMS_CONSUMER_2_HOURS_LEFT(booking):
    phone = booking.booked_by.user.phone_sms()
    return {
        'message_id': '136241',
        'variables_values': '{}|'.format(booking.store.name),
        'numbers': phone,
    }

def SMS_CONSUMER_SERVICE_STARTED(booking):
    store = booking.store
    event = booking.event
    seconds = (event.end_datetime - event.start_datetime).seconds
    phone = booking.booked_by.user.phone_sms()
    return {
        'message_id': '135922',
        'variables_values': '{}|{}'.format(store.name, secondsToTimeString(seconds)),
        'numbers': phone,
    }

def SMS_CONSUMER_SERVICE_COMPLETE(booking):
    phone = booking.booked_by.user.phone_sms()
    return {
        'message_id': '135920',
        'variables_values': '{}|'.format(booking.store.name),
        'numbers': phone,
    }

def SMS_CONSUMER_CANCELLATION_REQUESTED(booking):
    phone = booking.booked_by.user.phone_sms()
    return {
        'message_id': '135919',
        'variables_values': '{}|'.format(booking.booking_id),
        'numbers': phone,
    }

def SMS_CONSUMER_CANCELLATION_APPROVED(booking):
    phone = booking.booked_by.user.phone_sms()
    return {
        'message_id': '135918',
        'variables_values': '{}|{}'.format(booking.booking_id, booking.payment.amount),
        'numbers': phone,
    }

def SMS_CONSUMER_SERVICE_UNATTENDED(booking):
    phone = booking.booked_by.user.phone_sms()
    return {
        'message_id': '135917',
        'variables_values': '{}|'.format(booking.store.name),
        'numbers': phone,
    }

def SMS_OWNER_NEW_BOOKING(booking):
    vehicle_model = booking.vehicle_model
    event = booking.event
    phone = booking.store.owner.user.phone_sms()
    return {
        'message_id': '136242',
        'variables_values': '{}|{}|{}|{}|'.format(
            event.start_datetime.strftime('%d %b - %I:%M %p'),
            vehicle_model.brand,
            vehicle_model.model,
            float(booking.amount) - float(booking.payment.amount)
        ),
        'numbers': phone,
    }

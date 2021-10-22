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

def NOTIFICATION_BOOKING_COMPLETE(booking):
    store = booking.store
    vehicle_type = booking.vehicle_model.vehicle_type
    event = booking.event
    return {
        'title': 'Booking confirmed at {}'.format(store.name),
        'body': 'Your booking for {} {} on {} has been confirmed. Be sure to reach the store on time.'.format(vehicle_type.wheel, vehicle_type.model, event.start_datetime.strftime('%d %b')),
        'image': random_item(MODI_IMAGES)
    }

def NOTIFICATION_BOOKING_CANCELLED(booking):
    store = booking.store
    vehicle_type = booking.vehicle_model.vehicle_type
    event = booking.event
    return {
        'title': 'Booking cancelled at {}'.format(store.name),
        'body': 'Your booking for {} {} on {} has been cancelled. If you are not sure why this happened, feel free to contact us at {}'.format(vehicle_type.wheel, vehicle_type.model, event.start_datetime.strftime('%d %b'), CONTACT_EMAIL),
        'image': 'https://indianmemetemplates.com/wp-content/uploads/narendra-modi-angry-look.jpg'
    }

def NOTIFICATION_2_HOURS_LEFT(booking):
    store = booking.store
    return {
        'title': '2 Hours to go!',
        'body': 'Your booking at {} is in 2 hours. Hope to see you on time.'.format(store.name),
        'image': 'https://c.ndtvimg.com/2020-10/r5nivleo_pm-modi-invest-india-conference650_625x300_08_October_20.jpg'
    }

def NOTIFICATION_SERVICE_STARTED(booking):
    store = booking.store
    event = booking.event
    seconds = (event.end_datetime - event.start_datetime).seconds
    return {
        'title': 'You service at {} has been started'.format(store.name),
        'body': 'It will take around {} to get your vehicle ready. Thank you for your patience.'.format(secondsToTimeString(seconds)),
        'image': 'https://steamuserimages-a.akamaihd.net/ugc/946203347142688209/A8A976D7DB5A3D5658BA20D7CDD81E0EE83EB682/?imw=498&imh=318&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true'
    }

def NOTIFICATION_SERVICE_COMPLETED(booking):
    store = booking.store
    return {
        'title': 'You service at {} has been completed'.format(store.name),
        'body': 'Your vehicle is ready to be picked up. Hope you are happy with the services.',
        'image': 'https://i.ytimg.com/vi/YUwD1iwlLGU/hqdefault.jpg'
    }

def NOTIFICATION_SERVICE_UNATTENDED(booking):
    store = booking.store
    return {
        'title': 'Service Missed'.format(store.name),
        'body': 'No one appeared for your booking at {}. We hope that everything is fine and you are in good health.'.format(store.name),
        'image': 'https://media.millichronicle.com/2018/12/12121521/1432038380-1048.jpg'
    }

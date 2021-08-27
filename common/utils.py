import random
import string
import datetime
import math
from django.utils.text import slugify

def otp_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_unique_slug(model_instance, slugable_field_name, slug_field_name="slug"):
    """
    Takes a model instance, sluggable field name (such as 'title') of that
    model as string, slug field name (such as 'slug') of the model as string;
    returns a unique slug as string.
    """
    slug = slugify(getattr(model_instance, slugable_field_name))
    unique_slug = slug
    extension = 1
    model_class = model_instance.__class__

    while model_class._default_manager.filter(
        **{slug_field_name: unique_slug}
    ).exists():
        unique_slug = "{}-{}".format(slug, extension)
        extension += 1
    print(unique_slug)
    return unique_slug

def addToAverage(currentAverage, currentCount, newValue):
    '''
    Returns new average after adding another value
    '''
    oldSum = currentAverage * currentCount
    newSum = oldSum + newValue

    newAverage = newSum / (currentCount + 1)
    return newAverage

def removeFromAverage(currentAverage, currentCount, removeValue):
    '''
    Returns new average after removing a value
    '''
    if currentCount == 1:
        return 0
    
    oldSum = currentAverage * currentCount
    newSum = oldSum - removeValue
    
    newAverage = newSum / (currentCount - 1)
    return newAverage

def distanceFromLatitudeAndLongitude(latitude, longitude, latitude2, longitude2):
    '''
    Returns distance in kilo meters between two latitudes and longitudes
    '''
    latitude = float(latitude)
    longitude = float(longitude)
    latitude2 = float(latitude2)
    longitude2 = float(longitude2)
    
    radius = 6371
    dLat = math.radians(latitude2 - latitude)
    dLon = math.radians(longitude2 - longitude)
    lat1 = math.radians(latitude)
    lat2 = math.radians(latitude2)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

# Time Functions
def dateStringToDate(dateString):
    return datetime.datetime.strptime(dateString, '%Y-%m-%d')

def timeStringToTime(timeString):
    if len(timeString) == 5:
        return datetime.datetime.strptime(timeString, '%H:%M').time()
    else:
        return datetime.datetime.strptime(timeString, '%H:%M:%S').time()

def dateAndTimeStringsToDateTime(date, time):
    return datetime.datetime.strptime('{} {}'.format(date, time), '%Y-%m-%d %H:%M:%S')

def dateTimeDiffInMinutes(datetime1, datetime2):
    newTime = datetime1 - datetime2
    return newTime.seconds/60
import random
import string

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

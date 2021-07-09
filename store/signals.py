from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver

from store.models import *

@receiver(m2m_changed, sender=PriceTime.bays.through)
def updateBays(sender, instance, **kwargs):
    """
    Signal to add Vechicle Type to Bays' Supported Vehicle Types field
    """
    for bay in instance.bays.all():
        bay.supported_vehicle_types.add(instance.vehicle_type)


# @receiver(post_save, sender=PriceTime)
# def updateService(sender, instance, **kwargs):
#     """
#     Signal to add Vechicle Type to Service's Supported Vehicle Types field
#     """
#     instance.service.supported_vehicle_types.add(instance.vehicle_type)


@receiver(pre_delete, sender=PriceTime)
def updateServiceAndBays(sender, instance, **kwargs):
    """
    Signal to remove Vechicle Type from (Service's and Bay's) Supported Vehicle Types field
    """
    print(instance, instance.bays.all(), instance.service)

    # instance.service.supported_vehicle_types.remove(instance.vehicle_type)
    for bay in instance.bays.all():
        print("bay: ", bay)
        bay.supported_vehicle_types.remove(instance.vehicle_type)
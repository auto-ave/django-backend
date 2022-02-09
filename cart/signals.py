from django.db.models.signals import post_save, pre_delete, m2m_changed, pre_save
from django.dispatch import receiver

from cart.models import *

@receiver(m2m_changed, sender=Cart.items.through)
def updateCartValue(sender, instance, **kwargs):
    """
    Signal to update total, subTotal and taxes values when the cart is modified
    """
    instance.process_total()

@receiver(pre_save, sender=Cart)
def updateCart(sender, instance, **kwargs):
    """[summary]
    Signal to mainly process offer
    """
    instance.process_total()
    
    offer = instance.offer
    if offer:
        # offer = instance.offer
        # discount_percentage = offer.discount_percentage / 100 # since we store in percentage
        # max_discount = offer.max_discount
        
        # raw_discount = round(instance.subtotal * discount_percentage, 2)
        # if raw_discount > max_discount:
        #     raw_discount = max_discount
        
        # instance.discount = raw_discount
        raw_discount = offer.get_discount_amount_from_sub_total(instance.subtotal)
        instance.discount = raw_discount
        instance.total = instance.total - raw_discount
        for service in offer.services_to_add.all():
            price_time = PriceTime.objects.get(service=service, store=instance.store, vehicle_type=instance.vehicle_model.vehicle_type)
            instance.items.add(price_time)
    else:
        instance.discount = 0
        
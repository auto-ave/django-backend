from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver

from cart.models import *

@receiver(m2m_changed, sender=Cart.items.through)
def updateCartValue(sender, instance, **kwargs):
    """
    Signal to update total, subTotal and taxes values when the cart is modified
    """
    instance.subtotal = 0
    instance.total = 0
    for item in instance.items.all():
        instance.total += item.price
        instance.subtotal += item.price
    # TODO: Taxes bitch
    instance.save()

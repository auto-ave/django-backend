from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver

from booking.models import Review

@receiver(pre_delete, sender=Review)
def updateServiceAndBays(sender, instance, **kwargs):
    """
    Signal to edit store ratings when any review is getting deleted
    BUG: When deleting all the reviews together, rating doesn't go to None
    """
    instance.store.updateRating(instance.rating, True)
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from common.models import *
from accounts.models import NotificationTopic



@receiver(post_save, sender=City)
def createNotificationTopic(sender, instance, **kwargs):
    """
    Signal to create a Notification Topic when a City is created
    """
    NotificationTopic.objects.get_or_create(name=instance.name, code=instance.code)

@receiver(pre_delete, sender=City)
def deleteNotificationTopic(sender, instance, **kwargs):
    """
    Signal to delete a Notification Topic when a City is deleted
    """
    NotificationTopic.objects.filter(code=instance.code).delete()
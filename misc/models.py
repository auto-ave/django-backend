from django.db import models
from common.models import Model

from store.models import Store, Service

class StoreImage(Model):
    store = models.ForeignKey(Store, on_delete= models.CASCADE, related_name="images")
    image = models.ImageField()

    def __str__(self):
        return "{}: Image #{}".format(self.store.name, self.pk)

class ServiceImage(Model):
    service = models.ForeignKey(Service, on_delete= models.CASCADE, related_name="images")
    image = models.ImageField()

    def __str__(self):
        return "{}: Image #{}".format(self.store.name, self.pk)


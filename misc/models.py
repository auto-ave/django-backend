from django.db import models
from common.models import Model

from store.models import Store
from common.models import Service

class Feedback(Model):
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.email or self.phone

class ErrorLogging(Model):
    location = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    
from django.db import models
from common.models import Model

from store.models import Store
from common.models import Service

class Feedback(Model):
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(blank=True)
    order_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user

class Contact(Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ErrorLogging(Model):
    location = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    
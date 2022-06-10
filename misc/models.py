from django.db import models
from common.models import Model

from store.models import Store
from common.models import Service

from custom_admin_arrayfield.models.fields import ArrayField

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
    context = models.TextField(blank=True, null=True)
    exception = models.TextField(blank=True, null=True)
    traceback = models.TextField(blank=True, null=True)

class SendGridEmailEvent(Model):
    email = models.CharField(max_length=200, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    smtpId = models.CharField(max_length=300, null=True, blank=True)
    event = models.CharField(max_length=200, null=True, blank=True)
    category = ArrayField(base_field=models.CharField(max_length=200, null=True, blank=True), blank=True, null=True)
    sgEventId = models.CharField(max_length=200, null=True, blank=True)
    sgMessageId = models.CharField(max_length=300, null=True, blank=True)
    response = models.CharField(max_length=200, null=True, blank=True)
    reason = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    useragent = models.CharField(max_length=200, null=True, blank=True)
    ip = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)

class TransportEnquiry(Model):
    time = models.DateTimeField(auto_now_add=True)
    from_city = models.CharField(max_length=100, null=True, blank=True)
    to_city = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
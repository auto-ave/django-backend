from common.utils import get_unique_slug
from django.db import models
from custom_admin_arrayfield.models.fields import ArrayField
# from common.constants import VEHICLE_MODELS, VEHICLE_TYPES

class Model(models.Model):
    """
    Custom Abstract Model. Every other model needs to be inherited from it.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class City(Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)
    upcoming = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Cities'


class ServiceTag(Model):
    slug = models.SlugField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to="service_tags", default="/service_tags/default.png")
    banner = models.ImageField(upload_to="service_tags", default="/service_tags/banner.png")
    reputation = models.IntegerField(default=0, help_text="Used to order tags, higher reputation means higher priority")
    class Meta:
        ordering = ['-reputation']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(ServiceTag, self).save(*args, **kwargs)

class Service(Model):
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    images = ArrayField(base_field=models.URLField(), null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(ServiceTag, related_name='services', blank=True)
    reputation = models.IntegerField(default=0, help_text="Used to order services, higher reputation means higher priority")
    
    class Meta:
        ordering = ['-reputation']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


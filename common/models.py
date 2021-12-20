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
        return '{} : {}'.format(self.code, self.name)
    
    class Meta:
        verbose_name_plural = 'Cities'


class Service(Model):
    slug = models.SlugField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    images = ArrayField(base_field=models.URLField(), null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # self.code = self.code.lower()
        if not self.slug:
            self.slug = get_unique_slug(self, "name")
        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
from django.db import models
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
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.code = self.code.lower()
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return '{} : {}'.format(self.code, self.name)
    
    class Meta:
        verbose_name_plural = 'Cities'

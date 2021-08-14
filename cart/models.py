from store.models import Store
from django.db import models
from common.models import Model

from store.models import Store, PriceTime

class Cart(Model):
    consumer = models.OneToOneField('accounts.Consumer', on_delete=models.CASCADE, related_name="cart")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="carts", null=True)
    items = models.ManyToManyField(PriceTime, related_name="carts")

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Cart, self).save(*args, **kwargs)
    
    def addItem(self, item):
        if self.store != item.store:
            self.clear()
        self.items.add(item)
        self.store = item.store
        self.save()
    
    def removeItem(self, item):
        self.items.remove(item)
        self.save()

    def clear(self):
        self.items.clear()
    
    def complete(self):
        self.completed = True
        self.save()
    
    def is_valid(self):
        if not self.store:
            return False
        return True
    
    def total_time(self):
        time = 0
        for item in self.items.all():
            time += item.time_interval
        return time

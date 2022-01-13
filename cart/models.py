import vehicle
from store.models import Store
from django.db import models
from common.models import Model
from rest_framework.exceptions import ValidationError

from store.models import Store, PriceTime
from vehicle.models import VehicleModel

class Cart(Model):
    consumer = models.OneToOneField('accounts.Consumer', on_delete=models.CASCADE, related_name="cart")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="carts", null=True)
    items = models.ManyToManyField(PriceTime, related_name="carts")
    vehicle_model = models.ForeignKey('vehicle.VehicleModel', on_delete=models.SET_NULL, related_name="carts", null=True)

    offer = models.ForeignKey('booking.Offer', on_delete=models.SET_NULL, related_name="carts", null=True, blank=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Cart, self).save(*args, **kwargs)
    
    def addItem(self, item, vehicle_model_pk):
        vehicle_model = VehicleModel.objects.get(pk=vehicle_model_pk)
        print("request ka vehicle: ", vehicle_model)
        print("cart ka vehicle model: ", self.vehicle_model)

        if self.vehicle_model != vehicle_model:
            print('clear1')
            self.clear()

        if self.store != item.store:
            print('clear2')
            self.clear()
        
        old_items_vehicle_type = self.items.all().count() > 0 and self.items.all()[0].vehicle_type
        if item.vehicle_type != old_items_vehicle_type:
            print('clear3')
            self.clear()

        if item.vehicle_type != (self.vehicle_model and self.vehicle_model.vehicle_type):
            print('clear4')
            self.clear() 
        
        print(item.vehicle_type, vehicle_model and vehicle_model.vehicle_type)
        if item.vehicle_type != (vehicle_model and vehicle_model.vehicle_type):
            print('not clear but 5')
            raise ValidationError({
                'error': 'Store Item cannot be added for selected vehicle model'
            })
        
        self.items.add(item)
        self.store = item.store
        self.vehicle_model = vehicle_model          
        self.save()
    
    def removeItem(self, item):
        self.items.remove(item)
        if not self.items.all().count():
            self.vehicle_model = None
        self.save()

    def clear(self):
        self.items.clear()
        self.vehicle_model = None
        self.save()
    
    def complete(self):
        self.completed = True
        self.save()
    
    def is_valid(self):
        if not self.store:
            return False
        if not self.vehicle_model:
            return False
        return True
    
    def total_time(self):
        time = 0
        for item in self.items.all():
            time += item.time_interval
        return time

    def __str__(self):
        return "Cart: {}".format(self.consumer)

from booking.models import OfferRedeem
from booking.utils import get_commission_amount, get_commission_percentage
from common.utils import convert_date_to_datetime, daterange
import vehicle
from store.models import Store
from django.db import models
from common.models import Model
from rest_framework.exceptions import ValidationError

from store.models import Store, PriceTime
from vehicle.models import VehicleModel

import datetime

class Cart(Model):
    consumer = models.OneToOneField('accounts.Consumer', on_delete=models.CASCADE, related_name="cart")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="carts", null=True)
    items = models.ManyToManyField(PriceTime, related_name="carts")
    vehicle_model = models.ForeignKey('vehicle.VehicleModel', on_delete=models.SET_NULL, related_name="carts", null=True)

    offer = models.ForeignKey('booking.Offer', on_delete=models.SET_NULL, related_name="carts", null=True, blank=True)

    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Cart, self).save(*args, **kwargs)
    
    def process_total(self):
        if self.id:
            self.subtotal = 0
            self.total = 0
            for item in self.items.all():
                self.total += item.price
                self.subtotal += item.price
            Cart.objects.filter(pk=self.pk).update(
                subtotal=self.subtotal, total=self.total
            )
    
    def addItem(self, item, vehicle_model_pk):
        current_vehicle_model = self.vehicle_model
        current_store = self.store
        item_vehicle_type = item.vehicle_type
        vehicle_model = VehicleModel.objects.get(pk=vehicle_model_pk)
        
        old_items_vehicle_type = self.items.all().count() > 0 and self.items.all()[0].vehicle_type
        
        if item.is_offer:
            raise ValidationError({
                'error': 'You cannot add this item to cart, because it is an offer.'
            })
        
        if item_vehicle_type != (vehicle_model and vehicle_model.vehicle_type):
            raise ValidationError({
                'error': 'Store Item cannot be added for selected vehicle model'
            })

        if current_vehicle_model != vehicle_model:
            print('clear: vehicle model changed')
            self.clear()
        elif current_store != item.store:
            print('clear: store changed')
            self.clear()
        elif item_vehicle_type != old_items_vehicle_type:
            print('clear: vehicle type changed wrt old items')
            self.clear()
        elif item_vehicle_type != (current_vehicle_model and current_vehicle_model.vehicle_type):
            print('clear: vehicle type changed wrt current vehicle model')
            self.clear() 
        
        
        self.items.add(item)
        self.store = item.store
        self.vehicle_model = vehicle_model
        self.offer = None     
        self.save()
    
    def removeItem(self, item):
        self.items.remove(item)
        if not self.items.all().count():
            self.vehicle_model = None
        
        offer = self.offer
        if offer:
            flag = True
            applicable_services = offer.applicable_services.all()
            
            if applicable_services.count():
                if item.service not in applicable_services:
                    flag = False
            
            if flag:
                offer_services = offer.services_to_add.all()
                    
                if offer_services.count():
                    for service in offer_services:
                        price_time = PriceTime.objects.get(service=service, store=self.store, vehicle_type=self.vehicle_model.vehicle_type)
                        self.items.remove(price_time)

        self.offer = None
        self.save()

    def clear(self):
        self.items.clear()
        self.vehicle_model = None
        self.offer = None
        self.save()
    
    def booking_completed(self):
        if self.offer:
            OfferRedeem.objects.create(
                offer=self.offer,
                consumer=self.consumer,
            )
    
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
    
    def total_days(self):
        return self.total_time() // 1440
    
    def is_multi_day(self):
        if self.store:
            return self.total_time() >= self.store.intra_day_time
        else:
            False
    
    def get_estimate_finish_time(self, date: datetime.date) -> datetime.datetime:
        store = self.store
        
        ideal_complete_date = date + datetime.timedelta( days = self.total_days() )
        increment = 0
        for check_date in daterange(date, ideal_complete_date):
            print('is store close on {}: {}'.format(check_date, store.is_close(check_date)))
            if store.is_close(check_date):
                increment = increment + 1
        estimated_complete_date = ideal_complete_date + datetime.timedelta( days = increment )
        final_estimate = convert_date_to_datetime(estimated_complete_date, dummy_time=datetime.time(18, 0))
        
        return final_estimate

    def get_partial_pay_amount(self):
        amount = float(self.subtotal)
        commission_amount = get_commission_amount(amount)
        return round( commission_amount - float(self.discount) , 2)

    def __str__(self):
        return "Cart: {}".format(self.consumer)

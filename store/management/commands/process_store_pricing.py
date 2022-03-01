from django.core.management.base import BaseCommand
from django.db.models import Sum


from store.models import Store

import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        stores = Store.objects.all()
        for store in stores:
            price_rating = store.pricetimes.filter(vehicle_type__wheel__code__icontains='four', is_offer=False).aggregate(Sum('price'))['price__sum']
            print(f'setting price_rating for {store}: {price_rating}')
            if price_rating:
                store.price_rating = int(price_rating)
                store.save()
        
        
        
        
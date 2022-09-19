# Copy pricetimes from one store to another store

from store.models import Store

STORE_FROM = 'prestige-car-spa'
STORE_TO = 'clean-and-shine-car-spa-1'

store1 = Store.objects.get(slug=STORE_FROM)
store2 = Store.objects.get(slug=STORE_TO)

price_times = store1.pricetimes.all()

for pricetime in price_times:
    pricetime.id = None
    pricetime.store = store2
    pricetime.save()

print('voila!')
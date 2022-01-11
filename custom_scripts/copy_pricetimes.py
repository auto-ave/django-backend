# Copy pricetimes from one store to another store

from store.models import Store

STORE_1 = 'subodh'
STORE_2 = 'a1-car-wash'

store1 = Store.objects.get(slug=STORE_1)
store2 = Store.objects.get(slug=STORE_2)

price_times = store1.pricetimes.all()

for pricetime in price_times:
    pricetime.id = None
    pricetime.store = store2
    pricetime.save()

print('voila!')
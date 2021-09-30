from django.core.management.base import BaseCommand, CommandError
from store.models import *
from accounts.models import *
import json

class Command(BaseCommand):
    def handle(self, *args, **options):

        stores = []
        with open('miscellaneous/stores/stores.json') as json_file:
            stores = json.load(json_file)

        for store in stores:
            try:
                fields = store["fields"]
                salesman_user = User.objects.get(username='salesman')
                partner_user = User.objects.get(username='partner')
                owner_user = User.objects.get(username='aryaman')
                salesman = Salesman.objects.get(user=salesman_user)
                partner = Partner.objects.get(user=partner_user)
                owner = StoreOwner.objects.get(user=owner_user)
                city = City.objects.get_or_create(
                    code="bpl",
                    name="Bhopal",
                    latitude="23.2599000000000000",
                    longitude="77.4126000000000000",
                    upcoming=False
                )
                new_store = Store.objects.create(
                    salesman=salesman,
                    is_active=True,
                    is_verified_by_admin=True,
                    is_locked_for_salesman = False,
                    name = fields["name"],
                    slug = fields["slug"],
                    description = fields["description"],
                    thumbnail = fields["thumbnail"],
                    images = json.loads(fields["images"]),
                    contact_numbers = json.loads(fields["contact_numbers"]),
                    address = fields["address"],
                    latitude = fields["latitude"],
                    longitude = fields["longitude"],
                    merchant_id = fields["merchant_id"],
                    pincode = fields["pincode"],
                    email = fields["email"],
                    contact_person_name = fields["contact_person_name"],
                    contact_person_number = fields["contact_person_number"],
                    contact_person_photo = fields["contact_person_photo"],
                    store_times = json.loads(fields["store_times"]),
                    rating = fields["rating"],
                    city = city[0])

                if new_store.slug == "autobright-car-care":
                    new_store.partner = partner
                    new_store.owner = owner

                new_store.save()
            except:
                print('Store Already Exists with following data.')

        new_stores = Store.objects.all()
        for store in new_stores:
            for i in range(0,3):
                bay = Bay.objects.create(store=store)
                bay.save()

            vehicle_types = VehicleType.objects.all()
            services = Service.objects.all()
            for vehicle_type in vehicle_types:
                for service in services:
                    try:
                        pricetime = PriceTime.objects.create(
                            store = store,
                            service=service,
                            vehicle_type=vehicle_type,
                            description=service.description,
                            images = service.images,
                            price = 1000,
                            time_interval = 45
                        )
                        pricetime.save()
                    except:
                        print("PriceTime already exists with given data.")


        self.stdout.write(self.style.SUCCESS('Successfully created stores.'))
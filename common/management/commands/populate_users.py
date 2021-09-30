from django.core.management.base import BaseCommand, CommandError
from accounts.models import *
import json

class Command(BaseCommand):
    def handle(self, *args, **options):

        users = []
        with open('miscellaneous/users/users.json') as json_file:
            users = json.load(json_file)

        print(users)

        for user in users:
            try:
                fields = user["fields"]
                new_user = User.objects.create_user(
                    username=fields["username"],
                    password= "iitbhu",
                    first_name= fields["first_name"],
                    last_name= fields["last_name"],
                    phone = fields["phone"],
                    otp = fields["otp"],
                    email = fields["email"],
                    is_active=True)
                if new_user.username == 'subodhk' or new_user.username == 'aryaman':
                    new_user.is_superuser = True
                    new_user.is_staff = True
                    new_user.is_verified = True

                if new_user.username == 'salesman':
                    new_user.is_salesman = True

                if new_user.username == 'partner':
                    new_user.is_partner = True

                new_user.save()
            except:
                print("User already Exists.")

        salesman_user = User.objects.get(username='salesman')
        partner_user = User.objects.get(username='partner')
        owner_user = User.objects.get(username='aryaman')
        salesman = Salesman.objects.create(user=salesman_user)
        partner = Partner.objects.create(user=partner_user)
        owner = StoreOwner.objects.create(user=owner_user)

        self.stdout.write(self.style.SUCCESS('Successfully created users.'))
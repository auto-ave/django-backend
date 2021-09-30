from django.core.management.base import BaseCommand, CommandError
from django.core import management

class Command(BaseCommand):
    def handle(self, *args, **options):
        management.call_command('populate_vehicle_types')
        management.call_command('populate_bikes_brands')
        management.call_command('populate_cars_brands')
        management.call_command('populate_bikes')
        management.call_command('populate_cars')

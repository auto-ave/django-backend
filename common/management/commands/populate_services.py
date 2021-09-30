from django.core.management.base import BaseCommand, CommandError
from common.models import *
import json

class Command(BaseCommand):
    def handle(self, *args, **options):

        services = []
        with open('miscellaneous/services/services.json') as json_file:
            services = json.load(json_file)

        print(services)

        for service in services:
            fields = service["fields"]
            name = fields["name"]
            slug = fields["slug"]
            thumbnail = fields["thumbnail"]
            description = fields["description"]
            new_service = Service.objects.create(
                slug=slug,
                description = description,
                name = name,
                thumbnail = thumbnail)
            new_service.save()

        self.stdout.write(self.style.SUCCESS('Successfully created car models.'))
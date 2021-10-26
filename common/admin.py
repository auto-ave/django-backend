from django.contrib import admin

from django.forms import widgets
from django.db.models import JSONField
from .models import *

import json

class PrettyJSONWidget(widgets.Textarea):

    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            print("Error while rendering json")
            return super(PrettyJSONWidget, self).format_value(value)


class JsonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }



from common.models import City, Service
from custom_admin_arrayfield.admin.mixins import DynamicArrayMixin

admin.site.register(City)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin , DynamicArrayMixin):
    pass
    # readonly_fields = ("supported_vehicle_types", )

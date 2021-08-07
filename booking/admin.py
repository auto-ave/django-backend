from django.contrib import admin
from .models import *

class HiddenFieldsAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('booked_by', 'store'),
        }),
    )
    def get_readonly_fields(self, request, obj=None):
        # try:
        #     return [f.name for f in obj._meta.fields if not f.editable]
        # except:
        #     # if a new object is to be created the try clause will fail due to missing _meta.fields
        #     return ""
        if obj: # editing an existing object
            return ('booked_by', 'store')
        return self.readonly_fields

admin.site.register(Booking, HiddenFieldsAdmin)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(Review)

admin.site.register(Slot)
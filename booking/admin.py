from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Refund)
admin.site.register(Review)

admin.site.register(Slot)
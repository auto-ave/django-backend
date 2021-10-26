from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from custom_admin_arrayfield.admin.mixins import DynamicArrayMixin


class CustomUserAdmin(UserAdmin, DynamicArrayMixin):
    personalInfoSet = (
        'Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'otp')
        }
    )
    # notificationsInfoSet = (
    #     'Notifications', {
    #         'fields': ('fcm_tokens',)
    #     }
    # )
    fieldsets = (UserAdmin.fieldsets[0], personalInfoSet) + UserAdmin.fieldsets[2:]

admin.site.register(User, CustomUserAdmin)

admin.site.register(Consumer)
admin.site.register(StoreOwner)
admin.site.register(Partner)
admin.site.register(Salesman)
admin.site.register(Support)
admin.site.register(SubAdmin)

admin.site.register(NotificationTopic)
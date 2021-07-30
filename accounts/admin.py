from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    personalInfoSet = (
        'Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'otp')
        }
    )
    customPermissionsSet = (
        'Custom Permissions', {
            'fields': ('is_consumer', 'is_partner', 'is_salesman', 'is_support', 'is_sub_admin')
        }
    )
    fieldsets = (UserAdmin.fieldsets[0], personalInfoSet, customPermissionsSet) + UserAdmin.fieldsets[2:]

admin.site.register(User, CustomUserAdmin)

admin.site.register(Consumer)
admin.site.register(Partner)
admin.site.register(Salesman)
admin.site.register(Support)
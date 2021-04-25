from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    personalInfoSet = (
        'Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }
    )
    fieldsets = (UserAdmin.fieldsets[0], personalInfoSet) + UserAdmin.fieldsets[2:]

admin.site.register(User, CustomUserAdmin)

admin.site.register(Consumer)
admin.site.register(Partner)
admin.site.register(Salesman)
admin.site.register(Support)
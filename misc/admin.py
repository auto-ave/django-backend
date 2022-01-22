from misc.models import ErrorLogging, Feedback, Contact
from django.contrib import admin

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'order_id')
    search_fields = ( 'message', 'order_id' )

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ( 'name', 'email', 'message' )

@admin.register(ErrorLogging)
class ErrorLoggingAdmin(admin.ModelAdmin):
    list_display = ( 'exception' ,)
    search_fields = ( 'context', 'exception', 'traceback' )
from misc.models import *
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
    list_display = ( 'created_at', 'exception' ,)
    search_fields = ( 'created_at', 'updated_at', 'context', 'exception', 'traceback' )

@admin.register(SendGridEmailEvent)
class SendGridEmailEventAdmin(admin.ModelAdmin):
    list_display = ( 'email', 'timestamp', 'event', 'category', 'response', 'reason', 'status', 'useragent', 'ip', 'url' )
    search_fields = ( 'email', 'timestamp', 'smtpId', 'event', 'category', 'sgEventId', 'sgMessageId', 'response', 'reason', 'status', 'useragent', 'ip', 'url' )
    list_filter = ( 'event', )

@admin.register(TransportEnquiry)
class TransportEnquiryAdmin(admin.ModelAdmin):
    list_display = ( 'from_city', 'to_city', 'name', 'contact' )
    search_fields = ( 'from_city', 'to_city', 'name', 'contact' )
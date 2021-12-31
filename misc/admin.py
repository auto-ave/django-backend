from misc.models import ErrorLogging, Feedback
from django.contrib import admin

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'order_id')
    search_fields = ( 'message', 'order_id' )

@admin.register(ErrorLogging)
class ErrorLoggingAdmin(admin.ModelAdmin):
    list_display = ('location', 'content')
    search_fields = ( 'location', 'content' )
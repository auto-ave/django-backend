from misc.models import ErrorLogging, Feedback
from django.contrib import admin

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'message')
    search_fields = ( 'phone', 'email', 'message' )

@admin.register(ErrorLogging)
class ErrorLoggingAdmin(admin.ModelAdmin):
    list_display = ('location', 'content')
    search_fields = ( 'location', 'content' )
from misc.models import Feedback
from django.contrib import admin

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'message')
    search_fields = ( 'phone', 'email', 'message' )
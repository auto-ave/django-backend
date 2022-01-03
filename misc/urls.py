from django.urls import path

from misc.views import *

urlpatterns = [
    path('imageupload/', StoreImageUpload.as_view()),
    path('feedback/', FeedbackView.as_view()),
    path('contact/', ContactView.as_view()),
    
    path('danger/', DangerView.as_view()),
]
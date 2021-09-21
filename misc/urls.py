from django.urls import path

from misc.views import *

urlpatterns = [
    path('imageupload/', StoreImageUpload.as_view()),
    path('feedback/', FeedbackView.as_view())
]
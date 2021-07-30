from django.urls import path

from misc.views import *

urlpatterns = [
    path('imageupload/store', StoreImageUpload.as_view()),
    path('imageupload/service', ServiceImageUpload.as_view()),
]
from django.urls import path

from common.views import *

urlpatterns = [
    path('city/list', CityList.as_view()),
]
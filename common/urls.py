from django.urls import path

from common.views import *

urlpatterns = [
    path('city/list', CityList.as_view()),
    path('service/list/', ServiceList.as_view()),
    path('service/tag/list/', ServiceTagList.as_view()),
]
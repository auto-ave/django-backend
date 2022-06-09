from django.urls import path

from common.views import *

urlpatterns = [
    path('city/list', CityList.as_view()),
    path('service/list/', ServiceList.as_view()),
    path('service/tag/list/', ServiceTagList.as_view()),
    
    
    ## IRELAND URLS
    path('ie/city/list', CityList.as_view()),
    path('ie/service/list/', ServiceList.as_view()),
    path('ie/service/tag/list/', ServiceTagList.as_view()),
]
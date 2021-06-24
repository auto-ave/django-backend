from django.urls import path
from store.views import general

urlpatterns = [
    path('store/<slug:slug>/', general.StoreDetail.as_view()),
    path('storelist/',general.StoreList.as_view()),
    path('citystorelist/<str:city>/',general.CityStoreList.as_view()),
]
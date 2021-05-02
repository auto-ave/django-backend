from django.urls import path
from store.views import general

urlpatterns = [
    path('store/<int:pk>/', general.StoreDetail.as_view()),
    path('storelist/',general.StoreList.as_view()),
]
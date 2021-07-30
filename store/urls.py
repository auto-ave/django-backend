from django.urls import path
from store.views import general, review

urlpatterns = [
    path('store/<slug:slug>/', general.StoreDetail.as_view()),
    path('store/<slug:slug>/reviews', review.StoreReviewList().as_view()),

    path('store/list/',general.StoreList.as_view()),
    path('store/list/<str:citycode>/',general.CityStoreList.as_view()),
]
from django.urls import path
from store.views import general, review, services

urlpatterns = [
    path('store/<slug:slug>/', general.StoreDetail.as_view()),
    path('store/<slug:slug>/reviews', review.StoreReviewList().as_view()),
    path('store/<slug:slug>/services', services.StoreServicesList().as_view()),

    path('store/list/',general.StoreList.as_view()),
    path('store/list/<str:citycode>/',general.CityStoreList.as_view()),
        path('salesman/store/create/',general.CreateStoreGeneral.as_view()),
        path('salesman/servicecreationdetails/',general.ServiceCreationDetails.as_view()),
        path('salesman/pricetimes/',general.CreateStorePriceTimes.as_view()),
        path('salesman/<int:store>/services/',general.StoreServicesListOverview.as_view()),

]
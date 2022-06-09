from django.urls import path
from store.views import general, review, services, salesman

urlpatterns = [
    path('store/<slug:slug>/', general.StoreDetail.as_view()),
    path('store/<slug:slug>/reviews/', review.StoreReviewList().as_view()),
    path('store/<slug:slug>/services/', services.StoreServicesList().as_view()),

    path('store/list/',general.StoreList.as_view()),
    path('store/list/<str:citycode>/',general.CityStoreList.as_view()),
    path('store/list/<str:citycode>/featured/',general.CityStoreFeaturedList.as_view()),


    path('salesman/store/<slug:slug>/service/<int:pk>/', salesman.SalesmanStoreServiceRetrieve.as_view()),
    path('salesman/store/<slug:slug>/', salesman.SalesmanStoreRetrieve.as_view()),
    path('salesman/store/list/all/', salesman.SalesmanStoreList.as_view()),
    path('salesman/store/create', salesman.StoreCreateView.as_view()),
    path('salesman/store/update/<slug:slug>/', salesman.StoreUpdateView.as_view()),
    path('salesman/pricetimes/', salesman.CreateStorePriceTimes.as_view()),

    path('salesman/servicecreationdetails/<slug:slug>/', salesman.ServiceCreationDetails.as_view()),
    path('salesman/<slug:slug>/pricetimes/', salesman.StorePriceTimeList.as_view()),
    path('salesman/<slug:slug>/registration/email/', salesman.StoreRegistrationEmail.as_view()),
    
    
    
    
    ## IRELAND URLS
    path('ie/store/<slug:slug>/', general.StoreDetail.as_view()),
    path('ie/store/<slug:slug>/reviews/', review.StoreReviewList().as_view()),
    path('ie/store/<slug:slug>/services/', services.StoreServicesList().as_view()),

    path('ie/store/list/',general.StoreList.as_view()),
    path('ie/store/list/<str:citycode>/',general.CityStoreList.as_view()),
    path('ie/store/list/<str:citycode>/featured/',general.CityStoreFeaturedList.as_view()),


    path('ie/salesman/store/<slug:slug>/service/<int:pk>/', salesman.SalesmanStoreServiceRetrieve.as_view()),
    path('ie/salesman/store/<slug:slug>/', salesman.SalesmanStoreRetrieve.as_view()),
    path('ie/salesman/store/list/all/', salesman.SalesmanStoreList.as_view()),
    path('ie/salesman/store/create', salesman.StoreCreateView.as_view()),
    path('ie/salesman/store/update/<slug:slug>/', salesman.StoreUpdateView.as_view()),
    path('ie/salesman/pricetimes/', salesman.CreateStorePriceTimes.as_view()),

    path('ie/salesman/servicecreationdetails/<slug:slug>/', salesman.ServiceCreationDetails.as_view()),
    path('ie/salesman/<slug:slug>/pricetimes/', salesman.StorePriceTimeList.as_view()),
    path('ie/salesman/<slug:slug>/registration/email/', salesman.StoreRegistrationEmail.as_view()),
]
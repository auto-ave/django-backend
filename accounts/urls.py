from django.urls import path
from accounts.views import general, auth

urlpatterns = [
    path('account', general.ProfileView.as_view()),
    path('account/topics/register/', general.RegisterTopicsView.as_view()),
    path('account/topics/list/', general.TopicsList.as_view()),
    path('account/add_fcm/', general.AddToken.as_view()),
    
    path('consumer/login/sendOTP/', auth.AuthGetOTP.as_view()),
    path('consumer/login/checkOTP/', auth.AuthCheckOTP.as_view()),

    path('salesman/login/', auth.SalesmanLogin.as_view()),
    path('store-owner/login/', auth.StoreOwnerLogin.as_view())
]
from django.urls import path
from accounts.views import general, auth
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('account', general.ProfileView.as_view()),
    path('account/token/refresh', TokenRefreshView.as_view()),
    
    # path('account/topics/register/', general.RegisterTopicsView.as_view()),
    # path('account/topics/list/', general.TopicsList.as_view()),
    # path('account/add_fcm/', general.AddToken.as_view()),
    # path('account/remove_fcm/', general.RemoveToken.as_view()),
    
    path('consumer/login/sendOTP/', auth.AuthGetOTP.as_view()),
    path('consumer/login/checkOTP/', auth.AuthCheckOTP.as_view()),
    path('consumer/logout/app/', auth.AppLogout.as_view()),
    path('consumer/login/email/', auth.EmailLogin.as_view()),

    path('salesman/login/', auth.SalesmanLogin.as_view()),
    path('store-owner/login/', auth.StoreOwnerLogin.as_view()),
    
    
    ## IRELAND URLS
    path('ie/account', general.ProfileView.as_view()),
    path('ie/account/token/refresh', TokenRefreshView.as_view()),
    
    path('ie/consumer/login/sendOTP/', auth.AuthGetOTP.as_view()),
    path('ie/consumer/login/checkOTP/', auth.AuthCheckOTP.as_view()),
    path('ie/consumer/logout/app/', auth.AppLogout.as_view()),
    path('consumer/login/email/', auth.EmailLogin.as_view()),

    path('ie/salesman/login/', auth.SalesmanLogin.as_view()),
    path('ie/store-owner/login/', auth.StoreOwnerLogin.as_view())
]
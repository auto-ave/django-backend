from django.urls import path
from accounts.views import general, auth

urlpatterns = [
    path('account', general.ProfileView.as_view()),
    
    path('consumer/login/sendOTP/', auth.AuthGetOTP.as_view()),
    path('consumer/login/checkOTP/', auth.AuthCheckOTP.as_view()),
]
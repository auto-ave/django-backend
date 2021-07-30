from django.urls import path
from accounts.views import general, auth

urlpatterns = [
    path('account', general.ProfileView.as_view()),
    
    path('login/sendOTP/', auth.AuthGetOTP.as_view()),
]
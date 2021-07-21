from django.urls import path
from accounts.views import general

urlpatterns = [
    path('account', general.ProfileView.as_view()),
]
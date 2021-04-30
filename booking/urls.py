from django.urls import path
from booking.views import review

urlpatterns = [
    path('review/', review.ReviewListCreate.as_view()),
    # path('review/')
]
from django.urls import path
from booking.views import review

urlpatterns = [
    path('review/', review.ReviewListCreate.as_view()),
    path('store/<slug:slug>/reviews', review.StoreReviewList().as_view()),
    # path('review/')
]
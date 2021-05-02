from django.urls import path
from booking.views import review
from booking.views import general

urlpatterns = [
    path('review/', review.ReviewListCreate.as_view()),
    path('booking/consumer/list', general.BookingListConsumer.as_view()),   
    path('booking/partner/list', general.BookingListPartner.as_view()),   
    # booking/ motorwash k url mai daalna h ya yahi?  - motorwash mai dala toh booking/review sahi nahi lgega.
    # path('review/')
]
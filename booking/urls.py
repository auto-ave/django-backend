from django.urls import path
from booking.views import review, general, slots

urlpatterns = [
    path('review/', review.ReviewListCreate.as_view()),

    path('bookings/list/', general.BookingsList.as_view()),
    path('slots/create', slots.SlotCreate.as_view()),
]
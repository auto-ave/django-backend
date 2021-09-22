from django.urls import path
from booking.views import review, general, slots, payment

urlpatterns = [
    path('review/', review.ReviewListCreate.as_view()),
    path('review/<slug:booking_id>/', review.ReviewRetrieve.as_view()),

    path('booking/<str:booking_id>', general.BookingDetail.as_view()),
    path('booking/list/consumer', general.BookingsListConsumer.as_view()),

    path('slots/create', slots.SlotCreate.as_view()),

    path('payment/initiate/', payment.InitiateTransactionView.as_view()),
    path('payment/callback/', payment.PaymentCallbackView.as_view()),

    path('owner/booking/list/', general.BookingListOwner.as_view()),
    path('owner/service/start/', general.OwnerBookingStart.as_view()),
    path('owner/service/complete/', general.OwnerBookingComplete.as_view()),
    path('store-owner/revenue/', general.OwnerRevenue.as_view()),
    path('store-owner/new/bookings/',general.OwnerNewBookings.as_view()),
    path('store-owner/past/bookings/', general.OwnerPastBookings.as_view())
]
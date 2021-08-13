from django.urls import path
from booking.views import review, general, slots, payment

urlpatterns = [
    path('review/', review.ReviewListCreate.as_view()),

    path('booking/<str:booking_id>', general.BookingDetail.as_view()),
    path('booking/list/consumer', general.BookingsListConsumer.as_view()),
    path('booking/list/owner', general.BookingListOwner.as_view()),

    path('slots/create', slots.SlotCreate.as_view()),

    path('paytm', general.Paytm),
    path('initial', general.initiateTransaction),

    path('payment/initiate/', payment.InitiateTransactionView.as_view()),
    path('payment/callback/', payment.PaymentCallbackView.as_view()),
]
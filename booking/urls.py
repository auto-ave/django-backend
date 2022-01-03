from django.urls import path
from booking.views import offer, review, general, slots, payment, cancel

urlpatterns = [
    path('review/', review.ReviewListCreate.as_view()),
    path('review/<slug:booking_id>/', review.ReviewRetrieve.as_view()),

    path('booking/cancel/data/<str:booking_id>/', cancel.BookingCancelData.as_view()),
    path('booking/cancel/<str:booking_id>/', cancel.BookingCancel.as_view()),
    path('booking/<str:booking_id>/', general.BookingDetail.as_view()),
    path('booking/list/consumer/', general.BookingsListConsumer.as_view()),
    

    path('slots/create/', slots.SlotCreate.as_view()),
    
    path('payment/choices/', payment.PaymentChoices.as_view()),
    path('payment/initiate/', payment.InitiateTransactionView.as_view()),
    path('payment/callback/', payment.PaymentCallbackView.as_view()),

    path('owner/bookings/today/', general.OwnerTodayBookingsList.as_view()),
    path('owner/bookings/past/', general.OwnerPastBookingsList.as_view()),
    path('owner/bookings/upcoming/', general.OwnerUpcomingBookingsList.as_view()),
    path('owner/service/start/', general.OwnerBookingStart.as_view()),
    path('owner/service/complete/', general.OwnerBookingComplete.as_view()),
    
    path('store-owner/revenue/', general.OwnerRevenue.as_view()),
    path('store-owner/new/bookings/',general.OwnerUpcomingBookingsList.as_view()),
    path('store-owner/past/bookings/', general.OwnerPastBookingsList.as_view()),
    path('store-owner/store/vehicles/', general.OwnerStoreVehicleTypes.as_view()),
    path('store-owner/calender/', general.OwnerDayWiseCalender.as_view()),
    
    path('offer/list/', offer.OfferListView.as_view()),
    path('offer/banner/', offer.OfferBannerView.as_view()),
    path('offer/apply/', offer.OfferApplyView.as_view()),
]

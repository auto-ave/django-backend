from common.utils import DATETIME_NOW, DATETIME_TODAY_END, DATETIME_TODAY_START
from vehicle.models import VehicleModel
from booking.static import BookingStatusSlug
from common.mixins import ValidateSerializerMixin
from rest_framework import generics, permissions, response
from django.db.models import Q

from booking.models import *
from booking.serializers.general import *

from common.permissions import IsAuthenticated, IsConsumer, IsStoreOwner

from paytmchecksum import PaytmChecksum
import json, requests

from django.conf import settings
import datetime

class BookingsListConsumer(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = ( IsConsumer, )

    def get_queryset(self):
        user = self.request.user
        return user.consumer.bookings.all().order_by('-created_at')
            
class OwnerTodayBookingList(generics.ListAPIView):
    permission_classes = (IsStoreOwner, )
    serializer_class = BookingListOwnerSerializer

    def get_queryset(self):
        user = self.request.user
        
        success_status = BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_SUCCESS)
        service_started_status = BookingStatus.objects.get(slug=BookingStatusSlug.SERVICE_STARTED)
        
        return user.storeowner.store.bookings.filter(
            ( Q( event__start_datetime__contains=DATETIME_NOW.date() ))
            &
            ( Q( booking_status=success_status ) | Q( booking_status=service_started_status ) )
        )#.order_by('-booking_status_changed_time')

class BookingDetail(generics.RetrieveAPIView):
    lookup_field = 'booking_id'
    serializer_class = BookingDetailSerializer
    permission_classes = ( IsConsumer, )

    def get_queryset(self):
        return self.request.user.consumer.bookings.all()

class OwnerBookingStart(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = BookingStartSerializer
    permission_classes = (IsStoreOwner, )

    def post(self, request, *args, **kwargs):
        data = self.validate(request)
        booking_id = data['booking_id']
        otp = data['otp']

        booking = Booking.objects.get(booking_id=booking_id)

        if booking.store.owner.user != request.user:
            return response.Response({
                "error": "You are not allowed to start this booking"
            }, status=403)
        
        if booking.otp != otp:
            return response.Response({
                "error": "Invalid OTP"
            }, status=400)

        booking.start_service()

        return response.Response({
            "success": "Booking started"
        })





####################
## STORE OWNER VIEWS
####################
class OwnerBookingComplete(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = BookingCompleteSerializer
    permission_classes = (IsStoreOwner, )

    def post(self, request):
        data = self.validate(request)
        booking_id = data['booking_id']
        booking = Booking.objects.get(booking_id=booking_id)

        if booking.store.owner.user != request.user:
            return response.Response({
                "error": "You are not allowed to complete this booking"
            }, status=403)

        booking.complete_service()

        return response.Response({
            "success": "Booking Completed"
        })

class OwnerRevenue(generics.GenericAPIView):
    permission_classes = (IsStoreOwner, )

    def get(self, request):
        user = self.request.user
        bookings = user.storeowner.store.bookings.filter(
            Q( booking_status=BookingStatus.objects.get(BookingStatusSlug.SERVICE_COMPLETED) )
        )
        revenue = 0.0
        today = datetime.datetime.today().date()
        begin_date = today.replace(day=1)
        delta = datetime.timedelta(days=1)
        revenue_response = {}
        while begin_date <= today:
            day_bookings = user.storeowner.store.bookings.filter(
                Q( booking_status=BookingStatus.objects.get(BookingStatusSlug.SERVICE_COMPLETED) ) & 
                Q( event__start_datetime__contains=begin_date )
            )
            begin_date += delta
            for booking in day_bookings:
                if hasattr(booking, "amount"):
                    amount = float(booking.amount)
                    revenue += amount
            revenue_response[str(begin_date)] = revenue

        revenue_response["revenue"] = revenue

        return response.Response(revenue_response)

class OwnerStoreVehicleTypes(generics.GenericAPIView):
    permission_classes = (IsStoreOwner,)

    def get(self, request):
        vehicles = {}
        user = self.request.user
        bookings = user.storeowner.store.bookings.filter(
            Q( booking_status=BookingStatus.objects.get(BookingStatusSlug.SERVICE_COMPLETED) )
        )
        for booking in bookings:
            booking1 = BookingDetailSerializer(booking)
            vehicle_model = booking1["vehicle_model"]
            vehicle_model = VehicleModel.objects.filter(pk=vehicle_model).first()
            if vehicle_model:
                vehicle = vehicle_model.vehicle_type.name
                if vehicle.value in vehicles:
                    vehicles[vehicle.value] += 1
                else:
                    vehicles[vehicle.value] = 1

        return response.Response(vehicles)
class OwnerNewBookings(ValidateSerializerMixin, generics.GenericAPIView):
    permission_classes = (IsStoreOwner, )
    serializer_class = NewBookingListOwnerSerializer

    def get(self, request):
        user = self.request.user
        queryset = user.storeowner.store.bookings.filter(
            Q( booking_status=BookingStatus.objects.get(BookingStatusSlug.PAYMENT_SUCCESS) )
        ).order_by('-booking_status_changed_time')
        serializer = BookingListOwnerSerializer(queryset, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        user = self.request.user
        data = self.validate(request)
        date = data.get('date')
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        queryset = user.storeowner.store.bookings.filter(
            (
                Q( booking_status=BookingStatus.objects.get(BookingStatusSlug.PAYMENT_SUCCESS) ) | 
                Q( booking_status=BookingStatus.objects.get(BookingStatusSlug.SERVICE_STARTED) )
            )
            & 
            Q( event__start_datetime__contains=date.date() )
        ).order_by('event__start_datetime')
        serializer = BookingListOwnerSerializer(queryset, many=True)
        return response.Response(serializer.data)

class OwnerPastBookings(generics.ListAPIView):
    permission_classes = (IsStoreOwner, )
    serializer_class = BookingListOwnerSerializer

    def get_queryset(self):
        user = self.request.user
        return user.storeowner.store.bookings.filter(
            event__start_datetime__lt=datetime.datetime.today().date()
        ).order_by('-booking_status_changed_time')


class OwnerDayWiseCalender(generics.ListAPIView):
    permission_classes = (IsStoreOwner, )
    serializer_class = EventSerializer

    def get_queryset(self):
        user = self.request.user
        store = user.storeowner.store
        events = []
        bays = store.bays.all()
        for bay in bays:
            events.extend(bay.events.filter(
            start_datetime__gte=DATETIME_TODAY_START,
            end_datetime__lte=DATETIME_TODAY_END
        ).order_by('start_datetime'))
        return events
        
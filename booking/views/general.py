from common.utils import DATETIME_NOW, DATETIME_TODAY_END, DATETIME_TODAY_START, convert_date_to_datetime, daterange
from store.serializers.general import StoreDetailOwnerSerializer
from vehicle.models import VehicleModel
from booking.static import BookingStatusSlug
from common.mixins import ValidateSerializerMixin
from rest_framework import generics, permissions, response
from django.db.models import Q
from store.models import Event

from booking.models import *
from booking.serializers.general import *

from common.permissions import IsAuthenticated, IsConsumer, IsStoreOwner

from paytmchecksum import PaytmChecksum
import json, requests

from django.conf import settings
import datetime

##
## CONSUMER VIEWS
##
class BookingsListConsumer(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = ( IsConsumer, )

    def get_queryset(self):
        user = self.request.user
        initiated_status = BookingStatus.objects.get(slug=BookingStatusSlug.INITIATED)
        return user.consumer.bookings.filter(
            ~Q( booking_status=initiated_status )
        ).prefetch_related('booking_status', 'price_times', 'review', 'store', 'event').order_by('-created_at')

class BookingDetail(generics.RetrieveAPIView):
    lookup_field = 'booking_id'
    serializer_class = BookingDetailSerializer
    permission_classes = ( IsConsumer, )

    def get_queryset(self):
        return self.request.user.consumer.bookings.all()


##
## OWNER VIEWS
##
class OwnerTodayBookingsList(generics.ListAPIView):
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
        )

class OwnerPastBookingsList(generics.ListAPIView):
    permission_classes = (IsStoreOwner, )
    serializer_class = BookingListOwnerSerializer

    def get_queryset(self):
        user = self.request.user
        
        initiated_status = BookingStatus.objects.get(slug=BookingStatusSlug.INITIATED)
        payment_failed_status = BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_FAILED)
        
        return user.storeowner.store.bookings.filter(
            Q(
                event__start_datetime__lt=datetime.datetime.today().date()
            )
            &
            (
                ~Q( booking_status=initiated_status ) & ~Q( booking_status=payment_failed_status )
            )
        ).prefetch_related('vehicle_model', 'booked_by', 'payment', 'booking_status', 'event', 'price_times').order_by('-booking_status_changed_time')

class OwnerUpcomingBookingsList(generics.ListAPIView):
   
    permission_classes = (IsStoreOwner, )
    serializer_class = BookingListOwnerSerializer
    
    def get(self, request, *args, **kwargs):
        """
        NOTE - Provide 'date' in query parameters
        """
        return self.list(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        
        date = self.request.GET.get('date')
        if not date:
            date = DATETIME_NOW
        else:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')

        payment_success_status = BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_SUCCESS)
        
        return user.storeowner.store.bookings.filter(
                Q( booking_status=payment_success_status )
            &
                Q( event__start_datetime__contains=date.date() )
        ).order_by('event__start_datetime')


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

        if booking.booking_status != BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_SUCCESS):
            return response.Response({
                "error": "Invalid booking status, should be PAYMENT_SUCCESS"
            })
        
        booking.start_service()

        return response.Response({
            "success": "Booking started"
        })
    
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

        if booking.booking_status != BookingStatus.objects.get(slug=BookingStatusSlug.SERVICE_STARTED):
            return response.Response({
                "error": "Invalid Booking status, should be SERVICE_STARTED"
            })
        
        booking.complete_service()

        return response.Response({
            "success": "Booking Completed"
        })





####################
## STORE OWNER VIEWS
####################


class OwnerRevenue(generics.GenericAPIView):
    permission_classes = (IsStoreOwner, )
    serializer_class = OwnerRevenueSerializer

    def get(self, request):
        user = self.request.user
        bookings = user.storeowner.store.bookings.filter(
            Q( booking_status=BookingStatus.objects.get(slug=BookingStatusSlug.SERVICE_COMPLETED) )
        )
        revenue = 0.0
        today = datetime.datetime.today().date()
        begin_date = today.replace(day=1)
        delta = datetime.timedelta(days=1)
        revenue_response = {}
        while begin_date <= today:
            day_bookings = user.storeowner.store.bookings.filter(
                Q( booking_status=BookingStatus.objects.get(slug=BookingStatusSlug.SERVICE_COMPLETED) ) & 
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
    serializer_class = OwnerStoreVehicleTypesSerializer

    def get(self, request):
        vehicles = {}
        user = self.request.user
        bookings = user.storeowner.store.bookings.filter(
            Q( booking_status=BookingStatus.objects.get(slug=BookingStatusSlug.SERVICE_COMPLETED) )
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


class OwnerStoreDetail(generics.RetrieveAPIView):
    permission_classes = (IsStoreOwner, )
    serializer_class = StoreDetailOwnerSerializer
    
    def get_object(self):
        return self.request.user.storeowner.store

class OwnerCalenderBlock(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = CalenderBlockSerializer
    permission_classes = (IsStoreOwner,)
    
    def post(self, request):
        data = self.validate(request)
        user = self.request.user
        store = user.storeowner.store
        bays = store.bays.all()
        start_datetime = datetime.datetime.fromisoformat(data['start_datetime'])
        end_datetime = datetime.datetime.fromisoformat(data['end_datetime'])
        
        for bay in bays:
            if end_datetime.date() == start_datetime.date():
                Event.objects.create(
                    is_blocking=True,
                    bay=bay,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                )
            else:
                date_range = list(daterange(start_datetime.date(), end_datetime.date()))
                for index, date in enumerate(date_range):
                    if index == 0:
                        Event.objects.create(
                            is_blocking=True,
                            bay=bay,
                            start_datetime=start_datetime,
                            end_datetime=convert_date_to_datetime(date, dummy_time=datetime.time(23, 59)),
                        )
                    elif index == len(date_range) - 1:
                        Event.objects.create(
                            is_blocking=True,
                            bay=bay,
                            start_datetime=convert_date_to_datetime(date, dummy_time=datetime.time(0, 0)),
                            end_datetime=end_datetime,
                        )
                    else:
                        Event.objects.create(
                            is_blocking=True,
                            bay=bay,
                            start_datetime=convert_date_to_datetime(date),
                            end_datetime=convert_date_to_datetime(date, dummy_time=datetime.time(23, 59)),
                        )
        
        return response.Response({
            'success': 'Event created',
        })

class OwnerCalenderBlockList(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = (IsStoreOwner,)

    def get_queryset(self):
        user = self.request.user
        store = user.storeowner.store
        events = []
        bays = store.bays.all()
        events = Event.objects.filter(
            is_blocking=True,
            start_datetime__gte=DATETIME_TODAY_START,
            end_datetime__lte=DATETIME_TODAY_END,
            bay__in=bays
        ).distinct('start_datetime', 'end_datetime')
        return events

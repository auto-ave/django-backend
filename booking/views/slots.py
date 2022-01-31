from booking.static import BookingStatusSlug
from common.utils import DATETIME_NOW, DATETIME_TODAY_END, combineDateAndTime, convert_date_to_datetime, daterange, datetimeToBeautifulDateTime, timeStringToTime, timeToAMPMOnlyHour
from rest_framework import generics, response, status, permissions

from booking.serializers.slots import SlotCreateSerializer
from common.mixins import ValidateSerializerMixin
from booking.models import BookingStatus
from cart.models import Cart
from store.models import Event
from common.permissions import IsConsumer
from booking.models import Booking

from django.db.models import Prefetch
   
from collections import defaultdict
import datetime

class SlotCreate(ValidateSerializerMixin, generics.GenericAPIView):
    permission_classes = (IsConsumer,)
    serializer_class = SlotCreateSerializer

    def post(self, request):        
        def add_mins_to_time(timeval, mins_to_add):
            dummy_date = datetime.date(1, 1, 1)
            full_datetime = datetime.datetime.combine(dummy_date, timeval)
            added_datetime = full_datetime + datetime.timedelta(minutes=mins_to_add)
            return added_datetime.time()

        def add_mins_to_date_time(date_time, mins_to_add):
            added_datetime = date_time + datetime.timedelta(minutes=mins_to_add)
            return added_datetime
        
        def timeCollideCheck(start1, end1, start2, end2):
            if start1 < end2 and end1 > start2:
                return True
            else:
                return False
        
        def rounded_to_the_last_30th_minute_epoch():
            now = datetime.datetime.now()
            delta30 = ( datetime.timedelta(minutes=30) - (now - datetime.datetime.min) % datetime.timedelta(minutes=30) ) 
            return now + delta30
        
        data = self.validate(request)
        date = data.get('date')
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        print(date.date(), datetime.datetime.now().date())
        is_today = date.date() == datetime.datetime.now().date()

        user = request.user
        cart = user.consumer.get_cart()
        
        store = cart.store

        day = date.weekday()
        store_opening_time = timeStringToTime(store.store_times[day]['opening_time'])
        store_opening_time = combineDateAndTime(date, store_opening_time)
        store_closing_time = timeStringToTime(store.store_times[day]['closing_time'])
        store_closing_time  = combineDateAndTime(date, store_closing_time)
        
        if not store:
            return response.Response({
                "detail": "No store in cart"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(store.store_times) != 7:
            return response.Response({
                "detail": "Invalid Store Timings"
            }, status=status.HTTP_400_BAD_REQUEST)
        

        if not cart.is_valid():
            return response.Response({
                'detail': 'No Items in cart'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if cart.is_multi_day():
            estimated_complete_time = cart.get_estimate_finish_time(date)
            estimated_complete_time = datetimeToBeautifulDateTime(estimated_complete_time)
            slots = []
            breakpoint1 = combineDateAndTime(date, timeStringToTime("12:00:00"))
            breakpoint2 = combineDateAndTime(date, timeStringToTime("16:00:00"))
            
            if DATETIME_NOW < breakpoint1:
                slots.append({
                    'estimated_complete_time': estimated_complete_time,
                    'title': 'Morning',
                    'start_time': str( breakpoint1.time() if is_today else store_opening_time.time() ),
                    'time': f"{timeToAMPMOnlyHour(store_opening_time.time())} - {timeToAMPMOnlyHour(breakpoint1)}",
                    'image': 'https://cdn.autoave.in/population_data/sun+1.png'
                })
            if DATETIME_NOW < breakpoint2:
                slots.append({
                    'estimated_complete_time': estimated_complete_time,
                    'title': 'Afternoon',
                    'start_time': str( breakpoint2.time() if is_today else breakpoint1.time() ),
                    'time': f"{timeToAMPMOnlyHour(breakpoint1)} - {timeToAMPMOnlyHour(breakpoint2)}",
                    'image': 'https://cdn.autoave.in/population_data/sunset+1.png'
                })
            if DATETIME_NOW < store_closing_time:
                slots.append({
                    'estimated_complete_time': estimated_complete_time,
                    'title': 'Evening',
                    'start_time': str( store_closing_time.time() if is_today else breakpoint2.time() ),
                    'time': f"{timeToAMPMOnlyHour(breakpoint2)} - {timeToAMPMOnlyHour(store_closing_time.time())}",
                    'image': 'https://cdn.autoave.in/population_data/night+1.png'
                })

            return response.Response({
                'message': 'This is a multi day booking which will take more than one day to complete. You would be required to leave your vehicle at the service store for the desired time slot.',
                'delay_message': 'Exact completion time will be confirmed by the store owner.',
                'slots': slots
            })

        total_time = int(cart.total_time())
        OVERLAPING_SLOTS = total_time >= 90
        SLOT_INCREMENT = 60
        INCREMENT_TIME = SLOT_INCREMENT if OVERLAPING_SLOTS else total_time
        print(OVERLAPING_SLOTS, SLOT_INCREMENT, INCREMENT_TIME)

        print('total time: ', total_time)
        print('store opening time: ', store_opening_time, add_mins_to_date_time(store_opening_time, total_time))
        print('store ending time: ', store_closing_time, add_mins_to_date_time(store_closing_time, total_time))

        bays = store.bays.all()
        events = []

        # final_slots = defaultdict(lambda : bays_count)
        final_slots = {}
        # print('initial slots: ', final_slots)

        # Reset slot times
        print("is today: ", is_today)
        slot_start_time =  rounded_to_the_last_30th_minute_epoch() if is_today else store_opening_time # .strftime("%H:%M:%S") # store_opening_time
        slot_end_time = add_mins_to_date_time(slot_start_time, total_time)
        print('close time to epoch: ', rounded_to_the_last_30th_minute_epoch())
        print('initial slotsss----> ', slot_start_time, slot_end_time)
        print(type(slot_end_time))

        while(slot_end_time < store_closing_time):
            # print(slot_end_time, store_closing_time)
            string = '{} to {}'.format(slot_start_time.time(), slot_end_time.time())
            # print(string)
            # final_slots[string] = final_slots[string]
            final_slots[string] = [ bay.id for bay in bays ]
            
            # Update slot times
            slot_start_time = add_mins_to_date_time(slot_start_time, INCREMENT_TIME)
            slot_end_time = add_mins_to_date_time(slot_end_time, INCREMENT_TIME)
        
        print('pehla while loop khatam')
        booking_init_status = BookingStatus.objects.get(slug=BookingStatusSlug.INITIATED)
        for bay in bays:
            events = []
            
            events.extend(
                bay.events.prefetch_related(
                    Prefetch( 'booking', queryset=Booking.objects.select_related('booking_status') )
                ).filter(
                    start_datetime__gte=convert_date_to_datetime(date),
                    end_datetime__lte=convert_date_to_datetime(date + datetime.timedelta(days=1))
                )
            )

            events.extend(
                bay.events.prefetch_related(
                    Prefetch( 'booking', queryset=Booking.objects.select_related('booking_status') )
                ).filter(
                    is_blocking=True,
                    start_datetime__gte=datetime.datetime.now(),
                    end_datetime__gte=DATETIME_TODAY_END
                )
            )
            for event in events:
                if hasattr(event, 'booking') and event.booking.booking_status == booking_init_status:
                    continue
                # print('event: ', event)
                event_start_time = event.start_datetime
                event_end_time = event.end_datetime

                # Reset slot times
                slot_start_time = rounded_to_the_last_30th_minute_epoch() if is_today else store_opening_time
                slot_end_time = add_mins_to_date_time(slot_start_time, total_time)
                # print('initial slotsss----> ', slot_start_time, slot_end_time)

                while(slot_end_time < store_closing_time):
                    string = '{} to {}'.format(slot_start_time.time(), slot_end_time.time())
                    # print('slots----> ', slot_start_time, slot_end_time)
                    if timeCollideCheck(event_start_time, event_end_time, slot_start_time, slot_end_time):
                        # final_slots[string] = final_slots[string] - 1
                        if bay.id in final_slots[string]:
                            final_slots[string].remove(bay.id)
                        print('event and slot collided: ', event, slot_start_time, slot_end_time)
                    # else:
                    #     final_slots[string] = final_slots[string]
                    
                    # Update slot times
                    slot_start_time = add_mins_to_date_time(slot_start_time, INCREMENT_TIME)
                    slot_end_time = add_mins_to_date_time(slot_end_time, INCREMENT_TIME)
        
        count = 1
        final_response = []
        for key in final_slots:
            final_response.append({
                'key': count,
                'bay_ids': final_slots[key],
                'start': key.split(' to ')[0],
                'end': key.split(' to ')[1],
                # 'count': len(final_slots[key])
            })
            count = count + 1
            print('{} slots for {}'.format(final_slots[key], key))

        return response.Response(final_response, status=status.HTTP_200_OK)

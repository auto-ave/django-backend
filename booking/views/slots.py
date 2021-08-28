from common.utils import timeStringToTime
from rest_framework import generics, response, status, permissions

from booking.serializers.slots import SlotCreateSerializer
from common.mixins import ValidateSerializerMixin
from booking.models import Slot
from cart.models import Cart
from store.models import Event
from common.permissions import IsConsumer
   
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
        
        def convert_date_to_datetime(date):
            dummy_time = datetime.time(0, 0)

            full_datetime = datetime.datetime.combine(date, dummy_time)
            return full_datetime
        
        def timeCollideCheck(start1, end1, start2, end2):
            if start1 < end2 and end1 > start2:
                return True
            else:
                return False
        
        data = self.validate(request)
        date = data.get('date')
        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        user = request.user
        cart = user.consumer.get_cart()
        
        store = cart.store

        day = date.weekday()
        
        if len(store.store_times) != 7:
            return response.Response({
                "detail": "Invalid Store Timings"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        store_opening_time = timeStringToTime(store.store_times[day]['opening_time'])
        store_closing_time = timeStringToTime(store.store_times[day]['closing_time'])

        if not cart.is_valid():
            return response.Response({
                'detail': 'No Items in cart'
            }, status=status.HTTP_400_BAD_REQUEST)

        total_time = int(cart.total_time())
        print('total time: ', total_time)
        print('store opening time: ', store_opening_time, add_mins_to_time(store_opening_time, total_time))
        print('store ending time: ', store_closing_time, add_mins_to_time(store_closing_time, total_time))

        bays = store.bays.all()
        bays_count = bays.count()
        events = []

        # final_slots = defaultdict(lambda : bays_count)
        final_slots = {}
        # print('initial slots: ', final_slots)

        # Reset slot times
        slot_start_time = store_opening_time
        slot_end_time = add_mins_to_time(slot_start_time, total_time)
        # print('initial slotsss----> ', slot_start_time, slot_end_time)

        while(slot_end_time < store_closing_time):
            string = '{} to {}'.format(slot_start_time, slot_end_time)
            # final_slots[string] = final_slots[string]
            final_slots[string] = [ bay.id for bay in bays ]
            
            # Update slot times
            slot_start_time = add_mins_to_time(slot_start_time, total_time)
            slot_end_time = add_mins_to_time(slot_end_time, total_time)

        for bay in bays:
            events = bay.events.filter(start_datetime__gte=convert_date_to_datetime(date), end_datetime__lte=convert_date_to_datetime(date + datetime.timedelta(days=1)))
            for event in events:
                if hasattr(event, 'booking') and event.booking.status == 0:
                    continue
                # print('event: ', event)
                event_start_time = event.start_datetime.time()
                event_end_time = event.end_datetime.time()

                # Reset slot times
                slot_start_time = store_opening_time
                slot_end_time = add_mins_to_time(slot_start_time, total_time)
                # print('initial slotsss----> ', slot_start_time, slot_end_time)

                while(slot_end_time < store_closing_time):
                    string = '{} to {}'.format(slot_start_time, slot_end_time)
                    # print('slots----> ', slot_start_time, slot_end_time)
                    if timeCollideCheck(event_start_time, event_end_time, slot_start_time, slot_end_time):
                        # final_slots[string] = final_slots[string] - 1
                        if bay.id in final_slots[string]:
                            final_slots[string].remove(bay.id)
                        print('event and slot collided: ', event, slot_start_time, slot_end_time)
                    # else:
                    #     final_slots[string] = final_slots[string]
                    
                    # Update slot times
                    slot_start_time = add_mins_to_time(slot_start_time, total_time)
                    slot_end_time = add_mins_to_time(slot_end_time, total_time)
        
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

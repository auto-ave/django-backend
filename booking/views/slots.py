from rest_framework import generics, response, status

from booking.serializers.slots import SlotCreateSerializer
from common.mixins import ValidateSerializerMixin
from booking.models import Slot
from cart.models import Cart
from store.models import Event
   
from collections import defaultdict
import datetime

class SlotCreate(ValidateSerializerMixin, generics.GenericAPIView):
    serializer_class = SlotCreateSerializer

    def post(self, request):
        def timeDiff(time1,time2):
            timeA = datetime.datetime.strptime(time1, "%H:%M")
            timeB = datetime.datetime.strptime(time2, "%H:%M")
            print(timeA, timeB, type(timeA), type(time2))
            newTime = timeA - timeB
            return newTime.seconds/60
        
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
        cart = Cart.objects.get(pk=data.get('cart'))
        
        date = data.get('date')
        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        store = cart.store

        if not cart.isValid():
            return response.Response({
                'message': 'No Items in cart'
            }, status=status.HTTP_400_BAD_REQUEST)

        total_time = int(cart.total_time())
        print('total time: ', total_time)
        print('store opening time: ', store.opening_time, add_mins_to_time(store.opening_time, total_time))
        print('store ending time: ', store.closing_time, add_mins_to_time(store.closing_time, total_time))
        slot_length = store.slot_length

        bays = store.bays.all()
        bays_count = bays.count()
        events = []

        final_slots = defaultdict(lambda : bays_count)
        # print('initial slots: ', final_slots)

        # Reset slot times
        slot_start_time = store.opening_time
        slot_end_time = add_mins_to_time(slot_start_time, total_time)
        # print('initial slotsss----> ', slot_start_time, slot_end_time)

        while(slot_end_time < store.closing_time):
            string = '{} to {}'.format(slot_start_time, slot_end_time)
            final_slots[string] = final_slots[string]
            
            # Update slot times
            slot_start_time = add_mins_to_time(slot_start_time, total_time)
            slot_end_time = add_mins_to_time(slot_end_time, total_time)

        for bay in bays:
            events = bay.events.filter(start_datetime__gte=convert_date_to_datetime(date), end_datetime__lte=convert_date_to_datetime(date + datetime.timedelta(days=1)))
            
            for event in events:
                # print('event: ', event)
                event_start_time = event.start_datetime.time()
                event_end_time = event.end_datetime.time()

                # Reset slot times
                slot_start_time = store.opening_time
                slot_end_time = add_mins_to_time(slot_start_time, total_time)
                # print('initial slotsss----> ', slot_start_time, slot_end_time)

                while(slot_end_time < store.closing_time):
                    string = '{} to {}'.format(slot_start_time, slot_end_time)
                    # print('slots----> ', slot_start_time, slot_end_time)
                    if timeCollideCheck(event_start_time, event_end_time, slot_start_time, slot_end_time):
                        final_slots[string] = final_slots[string] - 1 
                        print('event and slot collided: ', event, slot_start_time, slot_end_time)
                    else:
                        final_slots[string] = final_slots[string]
                    
                    # Update slot times
                    slot_start_time = add_mins_to_time(slot_start_time, total_time)
                    slot_end_time = add_mins_to_time(slot_end_time, total_time)
            # print("events:")
            # for event in events:
            #     print(event.start_datetime.time(), event.end_datetime.time())
            #     events.append(event)
            
            # while(start < store.closing_time):
            #     # print(start, add_mins_to_time(start, store.slot_length))
            #     end = add_mins_to_time(start, store.slot_length)

            #     string = "{} from {}".format(start, end)

            #     for event in events:
            #         event_start = event.start_datetime.time()
            #         event_end = event.end_datetime.time()
            #         if event_end < start or event_start > end:
            #             print(start, end)
                        
            #             if final_slots.get(string):
            #                 final_slots[string] = final_slots[string] + 1
            #             else:
            #                 final_slots[string] = 1
            #             # final_slots.append(start)            
            #     start = add_mins_to_time(start, store.slot_length)
        
        final_response = []
        for key in final_slots:
            final_response.append({
                'start': key.split(' to ')[0],
                'end': key.split(' to ')[1],
                'count': final_slots[key]
            })
            print('{} slots for {}'.format(final_slots[key], key))
        
        
        # print(timeDiff(store.closing_time, store.opening_time))

        # slot = Slot(cart=cart, start_time="12:00", end_time="1:00")
        # slot.save()


        return response.Response(final_response, status=status.HTTP_200_OK)

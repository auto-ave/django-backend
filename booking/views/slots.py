from rest_framework import generics, response, status

from booking.serializers.slots import SlotCreateSerializer
from common.mixins import ValidateSerializerMixin
from booking.models import Slot
from cart.models import Cart
from store.models import Event

import datetime

class SlotCreate(ValidateSerializerMixin, generics.GenericAPIView):
    serializer_class = SlotCreateSerializer

    def post(self, request):
        data = self.validate(request)

        cart = Cart.objects.get(pk=data.get('cart'))
        date = data.get('date')
        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        store = cart.store

        if not cart.isValid():
            return response.Response({
                'message': 'No Items in cart'
            }, status=status.HTTP_400_BAD_REQUEST)

        total_time = cart.total_time()
        print(total_time)

        start = store.opening_time

        def timeDiff(time1,time2):
            timeA = datetime.datetime.strptime(time1, "%H:%M")
            timeB = datetime.datetime.strptime(time2, "%H:%M")
            print(timeA, timeB, type(timeA), type(time2))
            newTime = timeA - timeB
            return newTime.seconds/60
        
        def add_mins_to_time(timeval, secs_to_add):
            dummy_date = datetime.date(1, 1, 1)
            full_datetime = datetime.datetime.combine(dummy_date, timeval)
            added_datetime = full_datetime + datetime.timedelta(minutes=secs_to_add)
            return added_datetime.time()
        
        def convert_date_to_datetime(date):
            dummy_time = datetime.time(0, 0)
            print("dummy_time: ", dummy_time)
            full_datetime = datetime.datetime.combine(date, dummy_time)
            return full_datetime
        
        bays = store.bays.all()
        events = []

        final_slots = {}

        for bay in bays:
            start = store.opening_time
            events = bay.events.filter(start_datetime__gte=convert_date_to_datetime(date), end_datetime__lte=convert_date_to_datetime(date + datetime.timedelta(days=1)))
            
            # print("events:")
            # for event in events:
            #     print(event.start_datetime.time(), event.end_datetime.time())
            #     events.append(event)
            
            while(start < store.closing_time):
                # print(start, add_mins_to_time(start, store.slot_length))
                end = add_mins_to_time(start, store.slot_length)

                string = "{} from {}".format(start, end)

                for event in events:
                    event_start = event.start_datetime.time()
                    event_end = event.end_datetime.time()
                    if event_end < start or event_start > end:
                        print(start, end)
                        
                        if final_slots.get(string):
                            final_slots[string] = final_slots[string] + 1
                        else:
                            final_slots[string] = 1
                        # final_slots.append(start)            
                start = add_mins_to_time(start, store.slot_length)
            
        for key in final_slots:
            print('{} slots for {}'.format(final_slots[key], key))
        
        print("slots:")
        
        
        # print(timeDiff(store.closing_time, store.opening_time))

        # slot = Slot(cart=cart, start_time="12:00", end_time="1:00")
        # slot.save()


        return response.Response({
            'hello': 'workl'
        })

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
        date = data.get('datetime')
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
        
        while(start < store.closing_time):
            print(start, add_mins_to_time(start, store.slot_length))
            start = add_mins_to_time(start, store.slot_length)
        
        bays = store.bays.all()
        events = bays[0].events.filter(start_datetime__gte=convert_date_to_datetime(date))
        
        # print(timeDiff(store.closing_time, store.opening_time))

        # slot = Slot(cart=cart, start_time="12:00", end_time="1:00")
        # slot.save()


        return response.Response({
            'hello': 'workl'
        })

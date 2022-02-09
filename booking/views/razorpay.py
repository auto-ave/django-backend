# pylint: disable=unused-import
from os import stat
from httplib2 import Response
from booking.utils import check_event_collide_in_store, generate_booking_id
from misc.email_contents import EMAIL_CONSUMER_BOOKING_COMPLETE, EMAIL_CONSUMER_BOOKING_INITIATED, EMAIL_OWNER_NEW_BOOKING
from misc.notification_contents import NOTIFICATION_CONSUMER_2_HOURS_LEFT, NOTIFICATION_CONSUMER_BOOKING_COMPLETE, NOTIFICATION_CUSTOMER_BOOKING_INITIATED, NOTIFICATION_OWNER_NEW_BOOKING, NOTIFICATION_OWNER_BOOKING_INITIATED
from common.communication_provider import CommunicationProvider
from booking.static import BookingStatusSlug
from misc.sms_contents import SMS_CONSUMER_2_HOURS_LEFT, SMS_CONSUMER_BOOKING_COMPLETE, SMS_OWNER_NEW_BOOKING
from vehicle.models import VehicleType
from common.utils import dateAndTimeStringsToDateTime, dateStringToDate, dateTimeDiffInMinutes, randomUUID
from booking.utils import get_commission_percentage
from booking.serializers.payment import InitiateTransactionSerializer, PaymentChoicesSerializer, RazorPayPaymentCallbackSerializer
from rest_framework import generics, permissions, response, views, status
from django.conf import settings
from common.mixins import ValidateSerializerMixin

from store.models import Bay, Event
from booking.models import Booking, BookingStatus, Payment
from common.permissions import IsConsumer

from paytmchecksum import PaytmChecksum
import json, requests, datetime, uuid

import razorpay

razorpay_client = razorpay.Client(
    auth=(
        settings.RAZORPAY_ID,
        settings.RAZORPAY_SECRET
    )
)

class RazorPayInitiateTransactionView(ValidateSerializerMixin, generics.GenericAPIView):
    serializer_class = InitiateTransactionSerializer
    permission_classes = (IsConsumer,)
    
    def post(self, request):
        user = request.user
        data = self.validate(request)

        date = data.get('date') # Always Required
        bay = data.get('bay') # Required for single day bookings
        slot_start = data.get('slot_start') # Always required
        slot_end = data.get('slot_end') # Required for single day bookings
        
        start_datetime = dateAndTimeStringsToDateTime(date, slot_start)
        if start_datetime < datetime.datetime.now():
            return response.Response({
                'detail': 'Booking date and time should be in the future'
            })
        
        cart = user.consumer.get_cart()
        is_multi_day = cart.is_multi_day()
        
        if is_multi_day:
            bay = cart.store.bays.first()
            end_datetime = cart.get_estimate_finish_time(dateStringToDate(date))
            print('estimated finish time: ', end_datetime)
        else:
            if not bay:
                return response.Response({
                    'detail': 'Bay is required'
                })
            if not slot_end:
                return response.Response({
                    'detail': 'Slot end is required'
                })
            bay = Bay.objects.get(id=bay)
            end_datetime = dateAndTimeStringsToDateTime(date, slot_end)
        
        print('total cart time (in mins):' ,cart.total_time())
        if ( not is_multi_day ) and dateTimeDiffInMinutes(end_datetime, start_datetime) != cart.total_time():
            return response.Response({
                "detail": "Total time of booking should be equal to total time of cart"
            })
            
        if bay.store != cart.store:
            return response.Response({
                'detail': "The selected bay is not in the cart's store"
            })
        
        colliding_event = check_event_collide_in_store(start=start_datetime, end=end_datetime, store=bay.store)
        if colliding_event:
            return response.Response({
                "detail": "Slot colliding with other event",
                "event": str(colliding_event)
            })
        
        store = bay.store
        
        # Added commission amount coz currently we only using partial payment
        PAYMENT_AMOUNT = cart.get_partial_pay_amount() * 100 # in paisa
        print("PAYMENT_AMOUNT: ", PAYMENT_AMOUNT)
        
        data = {
            "amount": PAYMENT_AMOUNT,
            "currency": "INR",
            "notes": {
                "consumerId": user.consumer.id,
                "name": user.full_name(),
                "mobileNumber": str(user.phone),
                "store": bay.store.name,    
            },
        }
        payment = razorpay_client.order.create(data)
        print('razorpay payment: ', json.dumps(payment, indent=4))
        # payment response by razorpay
        # {
        #     "id": "order_IokNXiZnRR7rSB",
        #     "entity": "order",
        #     "amount": 83985,
        #     "amount_paid": 0,
        #     "amount_due": 83985,
        #     "currency": "INR",
        #     "receipt": null,
        #     "offer_id": null,
        #     "status": "created",
        #     "attempts": 0,
        #     "notes": {
        #         "consumerId": 1,
        #         "bookingId": "2D220DF7DB",
        #         "name": "Subodh Verma",
        #         "mobileNumber": "+918989820993",
        #         "store": "A1 car wash"
        #     },
        #     "created_at": 1643282294
        # }

        if payment:
            event = Event.objects.create(
                is_blocking=False,
                bay=bay,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
            )

            booking = Booking.objects.create(
                booking_id = generate_booking_id(),
                razorpay_order_id=payment['id'],
                booked_by = user.consumer,
                store = store,
                is_multi_day = is_multi_day,
                booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.INITIATED),
                event = event,
                amount = cart.total,
                vehicle_model = cart.vehicle_model,
            )

            for item in cart.items.all():
                booking.price_times.add(item)
            
            return response.Response({
                "key": settings.RAZORPAY_ID,
                "booking_id": booking.booking_id,
                "order_id": payment['id'],
                "amount": int(payment['amount']),
                "timeout": 500,
                "name": "Autoave Private Limited",
                "description": "Online Booking",
                "prefill": {
                    "name": user.full_name(),
                    "email": user.email,
                    "contact": str(user.phone_without_countrycode()),
                },
                "theme": {
                    "color": "#3570B5"
                }
            })
        else:
            return response.Response({
                'code': 69,
                "detail": 'No idea what went wrong, razorpay ki booking nhi bani'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RazorPayPaymentCallbackView(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = RazorPayPaymentCallbackSerializer
    permission_classes = (IsConsumer,)

    def post(self, request):
        user = request.user
        data = self.validate(request)
        
        cart = user.consumer.get_cart()
        
        booking_id = data.get('booking_id')
        razorpay_order_id = data.get('razorpay_order_id', None) # Optional fields
        razorpay_payment_id = data.get('razorpay_payment_id', None) # Optional fields
        razorpay_signature = data.get('razorpay_signature', None) # Optional fields
        
        try:
            booking = Booking.objects.get(booking_id=booking_id)
            # if is_failure:
            #     booking.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_FAILED)
            #     booking.booking_status_changed_time = datetime.datetime.now()
            #     booking.save()
            #     print('order was not successful because of verification error: ') 
            #     return response.Response({
            #         'detail': 'Payment failed'
            #     }, status=status.HTTP_400_BAD_REQUEST)
            
            if razorpay_order_id and ( razorpay_order_id != booking.razorpay_order_id ):
                return Response({
                    "detail": "Razorpay order id is not matching with booking order id"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            payment = Payment.objects.filter(booking=booking).exists()
            
            if payment:
                return response.Response({
                    "detail": "Payment already done"
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                Payment.objects.create(
                    status=data.get('STATUS'),
                    booking=booking,
                    transaction_id=razorpay_payment_id,
                    mode_of_payment=data.get('PAYMENTMODE'),
                    amount=cart.get_partial_pay_amount(), # very important, yah allah razorpay
                    gateway_name=data.get('GATEWAYNAME'),
                    bank_name=data.get('BANKNAME'),
                    payment_mode=data.get('PAYMENTMODE'),
                    rp_signature=razorpay_signature,
                )
        except Exception as e:
            return response.Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
        except Exception as e:
            booking.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_FAILED)
            booking.booking_status_changed_time = datetime.datetime.now()
            booking.offer = cart.offer
            booking.save()
            print('order was not successful because of verification error: ') 
            return response.Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
            
        booking.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_SUCCESS)
        booking.booking_status_changed_time = datetime.datetime.now()
        booking.offer = cart.offer
        booking.save()
        
        # Payment confirmation notification for Consumer
        CommunicationProvider.send_notification(
            **NOTIFICATION_CONSUMER_BOOKING_COMPLETE(booking)
        )
        CommunicationProvider.send_sms(
            **SMS_CONSUMER_BOOKING_COMPLETE(booking)
        )
        if user.email:
            CommunicationProvider.send_email(
                **EMAIL_CONSUMER_BOOKING_COMPLETE(booking)
            )
        
        # Payment confirmation notification for Store Owner
        store = booking.store
        if store.owner:
            CommunicationProvider.send_notification(
                **NOTIFICATION_OWNER_NEW_BOOKING(booking),
            )
            CommunicationProvider.send_sms(
                **SMS_OWNER_NEW_BOOKING(booking)
            )
        if store.email:
            CommunicationProvider.send_email(
                **EMAIL_OWNER_NEW_BOOKING(booking)
            )


        CommunicationProvider.send_notification(
            **NOTIFICATION_CONSUMER_2_HOURS_LEFT(booking),
            schedule=(booking.event.start_datetime - datetime.timedelta(hours=2))
        )
        CommunicationProvider.send_sms(
            **SMS_CONSUMER_2_HOURS_LEFT(booking),
            schedule=(booking.event.start_datetime - datetime.timedelta(hours=2))
        )

        booking.booking_unattended_check(booking.booking_id, schedule=booking.event.end_datetime )

        # clear cart after order successfull
        user.consumer.cart.booking_completed()
        user.consumer.cart.clear()
        
        print('order successful')
            
        
        return response.Response(data) 
        
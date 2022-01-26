# pylint: disable=unused-import
from booking.utils import check_event_collide_in_store, generate_booking_id
from misc.email_contents import EMAIL_CONSUMER_BOOKING_COMPLETE, EMAIL_CONSUMER_BOOKING_INITIATED, EMAIL_OWNER_NEW_BOOKING
from misc.notification_contents import NOTIFICATION_CONSUMER_2_HOURS_LEFT, NOTIFICATION_CONSUMER_BOOKING_COMPLETE, NOTIFICATION_CUSTOMER_BOOKING_INITIATED, NOTIFICATION_OWNER_NEW_BOOKING, NOTIFICATION_OWNER_BOOKING_INITIATED
from common.communication_provider import CommunicationProvider
from booking.static import BookingStatusSlug
from misc.sms_contents import SMS_CONSUMER_2_HOURS_LEFT, SMS_CONSUMER_BOOKING_COMPLETE, SMS_OWNER_NEW_BOOKING
from vehicle.models import VehicleType
from common.utils import dateAndTimeStringsToDateTime, dateStringToDate, dateTimeDiffInMinutes, randomUUID
from booking.utils import get_commission_percentage
from booking.serializers.payment import InitiateTransactionSerializer, PaymentChoicesSerializer
from rest_framework import generics, permissions, response,views
from django.conf import settings
from common.mixins import ValidateSerializerMixin

from store.models import Bay, Event
from booking.models import Booking, BookingStatus, Payment
from common.permissions import IsConsumer

from paytmchecksum import PaytmChecksum
import json, requests, datetime, uuid

class PaymentChoices(generics.GenericAPIView):
    permission_classes = (IsConsumer,)
    serializer_class = PaymentChoicesSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        cart = user.consumer.get_cart()
        total_amount = float(cart.total)
        commission_amount = cart.get_partial_pay_amount()
        
        payment_choices = [
            {
                "type": "FULL",
                "title": "Pay in Full",
                "description": "Pay the full amount right now and book the service",
                "active": False,
                "amount": total_amount,
                "remaining_amount": 0
            },
            {
                "type": "PARTIAL",
                "title": "Pay Partially",
                "description": "Pay only the booking amount to confirm your slot. Remaining amount will be paid at the store.",
                "active": True,
                "amount": commission_amount,
                "remaining_amount": total_amount - commission_amount
            }
        ]
        return response.Response(payment_choices)


class InitiateTransactionView(ValidateSerializerMixin, generics.GenericAPIView):
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

        event = Event.objects.create(
            is_blocking=False,
            bay=bay,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

        booking = Booking.objects.create(
            booking_id = generate_booking_id(),
            booked_by = user.consumer,
            store = bay.store,
            is_multi_day = is_multi_day,
            booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.INITIATED),
            event = event,
            amount = cart.total,
            vehicle_model = cart.vehicle_model,
        )

        for item in cart.items.all():
            booking.price_times.add(item)


        # Just testing notifis
        # Payment confirmation notification for Store Owner
        store = booking.store
        # CommunicationProvider.send_notification(
        #     **NOTIFICATION_CUSTOMER_BOOKING_INITIATED(booking),
        # )
        if store.owner:
            CommunicationProvider.send_notification(
                **NOTIFICATION_OWNER_BOOKING_INITIATED(booking),
            )
            # if store.email or store.owner.user.email:
            #     CommunicationProvider.send_email(
            #         **EMAIL_OWNER_BOOKING_COMPLETE(booking)
            #     )



        ORDER_ID = booking.booking_id
        
        # Added commission amount coz currently we only using partial payment
        PAYMENT_AMOUNT = str(cart.get_partial_pay_amount())
        print("PAYMENT_AMOUNT: ", PAYMENT_AMOUNT)
        
        CALLBACK_URL = "https://{}/payment/callback/".format(request.get_host()) 
        CALLBACK_URL = settings.PAYTM_BASE_URL + "/paytmCallback?ORDER_ID={}".format(ORDER_ID)

        paytmParams = dict()
        paytmParams["body"] = {
            "requestType" : "Payment",
            "mid": settings.PAYTM_MID,
            "websiteName": settings.PAYTM_WEBSITE_NAME,
            "orderId": ORDER_ID,
            "callbackUrl": CALLBACK_URL,
            "txnAmount": {
                "value": PAYMENT_AMOUNT,
                "currency": settings.PAYTM_CURRENCY,
            },
            "userInfo": {
                "custId": user.consumer.id,
                "name": user.full_name(),
                "mobileNumber": str(user.phone),
                "store": bay.store.name,
            },
        }

        # Generate checksum by parameters we have in body
        # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
        checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), settings.PAYTM_MKEY)

        paytmParams["head"] = {
            "signature": checksum
        }

        post_data = json.dumps(paytmParams)

        url = settings.PAYTM_BASE_URL +  "/api/v1/initiateTransaction?mid={}&orderId={}".format(settings.PAYTM_MID, ORDER_ID)

        resp = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
        body = resp["body"]
        print('order create body: ', body)

        if body['resultInfo']['resultStatus'] == "S":
            return response.Response({
                "mid": settings.PAYTM_MID,
                "order_id": ORDER_ID,
                "amount": PAYMENT_AMOUNT,
                "callback_url": CALLBACK_URL,
                "txn_token": body['txnToken']
            })
        else:
            return response.Response({
                'code': body['resultInfo']['resultCode'],
                "detail": body['resultInfo']['resultMsg']
            })

class PaymentCallbackView(views.APIView):
    permission_classes = (IsConsumer,)

    def post(self, request):
        data = request.data
        user = request.user

        checksum = ""

        booking = ""
        
        try:
            checksum = data['CHECKSUMHASH']
            orderid = data['ORDERID']
            
            booking = Booking.objects.get(booking_id=orderid)
            payment = Payment.objects.filter(booking=booking).exists()
            
            if payment:
                return response.Response({
                    "detail": "Payment already done"
                })
            else:
                Payment.objects.create(
                    status=data.get('STATUS'),
                    booking=booking,
                    transaction_id=data.get('TXNID'),
                    mode_of_payment=data.get('PAYMENTMODE'),
                    amount=data.get('TXNAMOUNT'),
                    gateway_name=data.get('GATEWAYNAME'),
                    bank_name=data.get('BANKNAME'),
                    payment_mode=data.get('PAYMENTMODE')
                )
        except Exception as e:
            return response.Response({
                'error': str(e)
            })

        verify = PaytmChecksum.verifySignature(data, settings.PAYTM_MKEY, checksum)

        if verify:
            if data['RESPCODE'] == '01':
                booking.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_SUCCESS)
                booking.booking_status_changed_time = datetime.datetime.now()
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
            else:
                booking.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_FAILED)
                booking.booking_status_changed_time = datetime.datetime.now()
                booking.save()
                print('order was not successful because' + data['RESPMSG']) 
            
            return response.Response(data) 
        else:
            print('checksum verification failed')
            data['youare'] = 'a rendi, checksum failed'
            data['verificationresult'] = str(verify)
            return response.Response(data) 
            return response.Response({
                "you are": "a rendi"
            })
        
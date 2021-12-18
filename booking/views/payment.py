# pylint: disable=unused-import
from booking.utils import check_event_collide, generate_booking_id, get_commission_amount
from misc.email_contents import EMAIL_CONSUMER_BOOKING_COMPLETE, EMAIL_CONSUMER_BOOKING_INITIATED, EMAIL_OWNER_BOOKING_COMPLETE
from misc.notification_contents import NOTIFICATION_CONSUMER_2_HOURS_LEFT, NOTIFICATION_CONSUMER_BOOKING_COMPLETE, NOTIFICATION_OWNER_BOOKING_COMPLETE, NOTIFICATION_OWNER_BOOKING_INITIATED
from common.communication_provider import CommunicationProvider
from booking.static import BookingStatusSlug
from vehicle.models import VehicleType
from common.utils import dateAndTimeStringsToDateTime, dateStringToDate, dateTimeDiffInMinutes, randomUUID
from booking.utils import get_commission_percentage
from booking.serializers.payment import InitiateTransactionSerializer
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
    
    def get(self, request, *args, **kwargs):
        user = request.user
        cart = user.consumer.get_cart()
        total_amount = float(cart.total)
        commission_amount = get_commission_amount(total_amount)
        
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

        date = data.get('date')
        bay = data.get('bay')
        bay = Bay.objects.get(id=bay)

        slot_start = data.get('slot_start')
        slot_end = data.get('slot_end')

        start_datetime = dateAndTimeStringsToDateTime(date, slot_start)
        end_datetime = dateAndTimeStringsToDateTime(date, slot_end)

        print(start_datetime, end_datetime)

        cart = user.consumer.get_cart()
        print(dateTimeDiffInMinutes(end_datetime, start_datetime), cart.total_time())
        if dateTimeDiffInMinutes(end_datetime, start_datetime) != cart.total_time():
            return response.Response({
                "detail": "Total time of booking should be equal to total time of cart"
            })
        
        if check_event_collide(start=start_datetime, end=end_datetime, store=bay.store):
            return response.Response({
                "detail": "Slot colliding with other event"
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
            booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.INITIATED),
            event = event,
            amount = cart.total,
            vehicle_model = cart.vehicle_model,
        )
        # booking.event = event
        for item in cart.items.all():
            booking.price_times.add(item)
        # booking.price_times.set([cart.items.all()])
        # booking.save()


        # Just testing notifis
        # Payment confirmation notification for Store Owner
        store = booking.store
        if store.has_owner():
            CommunicationProvider.send_notification(
                **NOTIFICATION_OWNER_BOOKING_INITIATED(booking),
            )
            # if store.email or store.owner.user.email:
            #     CommunicationProvider.send_email(
            #         **EMAIL_OWNER_BOOKING_COMPLETE(booking)
            #     )

        print("total: ", cart.total, str(cart.total))
        ORDER_ID = booking.booking_id
        # Added commission amount coz currently we only using partial payment
        PAYMENT_AMOUNT = str(get_commission_amount(cart.total))
        CALLBACK_URL = "https://{}/payment/callback/".format(request.get_host()) 
        CALLBACK_URL = "https://securegw-stage.paytm.in/theia/paytmCallback?ORDER_ID={}".format(ORDER_ID)

        paytmParams = dict()
        paytmParams["body"] = {
            "requestType" : "Payment",
            "mid": settings.PAYTM_MID,
            "websiteName": "WEBSTAGING",
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

        # for Staging
        url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={}&orderId={}".format(settings.PAYTM_MID, ORDER_ID)

        # for Production
        # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
        resp = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
        body = resp["body"]

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
                "detail": body['resultInfo']['resultMessage']
            })

class PaymentCallbackView(views.APIView):
    permission_classes = (IsConsumer,)

    def post(self, request):
        data = request.data
        user = request.user

        checksum = ""
        form = data

        booking = ""

        response_dict = {}

        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                checksum = form[i]
            if i == 'ORDERID':
                print('paytm ki ma ki chut')
                booking = Booking.objects.get(booking_id=form.get('ORDERID'))
                if Payment.objects.filter(booking=booking).exists():
                    return response.Response({
                        "detail": "Payment already done"
                    })
                else:
                    payment = Payment.objects.create(
                        status=form.get('STATUS'),
                        booking=booking,
                        transaction_id=form.get('TXNID'),
                        mode_of_payment=form.get('PAYMENTMODE'),
                        amount=form.get('TXNAMOUNT'),
                        gateway_name=form.get('GATEWAYNAME'),
                        bank_name=form.get('BANKNAME'),
                        payment_mode=form.get('PAYMENTMODE')
                    )

        verify = PaytmChecksum.verifySignature(response_dict, settings.PAYTM_MKEY, checksum)

        if verify:
            if response_dict['RESPCODE'] == '01':
                booking.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_SUCCESS)
                booking.booking_status_changed_time = datetime.datetime.now()
                
                # Payment confirmation notification for Consumer
                CommunicationProvider.send_notification(
                    **NOTIFICATION_CONSUMER_BOOKING_COMPLETE(booking),
                )
                if user.email:
                    CommunicationProvider.send_email(
                        **EMAIL_CONSUMER_BOOKING_COMPLETE(booking)
                    )
                
                # Payment confirmation notification for Store Owner
                store = booking.store
                if store.has_owner():
                    CommunicationProvider.send_notification(
                        **NOTIFICATION_OWNER_BOOKING_COMPLETE(booking),
                    )
                    if store.email or store.owner.user.email:
                        CommunicationProvider.send_email(
                            **EMAIL_OWNER_BOOKING_COMPLETE(booking)
                        )


                CommunicationProvider.send_notification(
                    **NOTIFICATION_CONSUMER_2_HOURS_LEFT(booking),
                    schedule=(booking.event.start_datetime - datetime.timedelta(hours=2))
                )

                booking.booking_unattended_check(booking.booking_id, schedule=booking.event.end_datetime )

                print('order successful')
            else:
                booking.booking_status = BookingStatus.objects.get(slug=BookingStatusSlug.PAYMENT_FAILED)
                booking.booking_status_changed_time = datetime.datetime.now()
                print('order was not successful because' + response_dict['RESPMSG'])
            
            # clear cart
            user.consumer.cart.clear()

            booking.save()
            return response.Response(response_dict)  
        else:
            print('checksum verification failed')
            return response.Response({
                "you are": "a rendi"
            })
        
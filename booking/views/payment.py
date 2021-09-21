from common.communication_provider import CommunicationProvider
from booking.static import BOOKING_STATUS_DICT
from vehicle.models import VehicleType
from common.utils import dateAndTimeStringsToDateTime, dateStringToDate, dateTimeDiffInMinutes
from booking.serializers.payment import InitiateTransactionSerializer
from rest_framework import generics, permissions, response,views
from django.conf import settings
from common.mixins import ValidateSerializerMixin

from store.models import Bay, Event
from booking.models import Booking, Payment
from common.permissions import IsConsumer

from paytmchecksum import PaytmChecksum
import json, requests, datetime, uuid



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

        event = Event.objects.create(
            is_blocking=False,
            bay=bay,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

        booking = Booking.objects.create(
            booking_id=uuid.uuid4().hex[:6].upper(),
            booked_by = user.consumer,
            store = bay.store,
            status = 0,
            event = event,
            amount = cart.total,
            # TODO:
            vehicle_type = cart.items.all().first().vehicle_type,
        )
        # booking.event = event
        for item in cart.items.all():
            booking.price_times.add(item)
        # booking.price_times.set([cart.items.all()])
        # booking.save()

        print("total: ", cart.total, str(cart.total))
        ORDER_ID = booking.booking_id
        AMOUNT = str(cart.total)
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
                "value": AMOUNT,
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
                "amount": AMOUNT,
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
                booking.status = BOOKING_STATUS_DICT.PAYMENT_DONE.value
            
                
                # Payment complete notification
                CommunicationProvider.send_notification(
                    user,
                    title="Booking Confirmed ho gai hai aapki",
                    body="Thank you sir aapni booking kari, aapke hum aabhari hai. Store chale jana time se ok, thank you.",
                    image="https://i.tribune.com.pk/media/images/1038308-MODI-1454343716/1038308-MODI-1454343716.jpg",
                    data={}
                )

                CommunicationProvider.send_notification(
                    user,
                    title="6 hours to go!",
                    body="hello bro, time aane wala hai",
                    image="https://pbs.twimg.com/media/Dtb9LYCXQAAqBE6.jpg",
                    data={},
                    schedule=datetime.now() + datetime.timedelta(hours=6)
                )

                print('order successful')
            else:
                booking.status = BOOKING_STATUS_DICT.PAYMENT_FAILED.value
                print('order was not successful because' + response_dict['RESPMSG'])
            booking.save()
            return response.Response(response_dict)  
        else:
            print('checksum verification failed')
            return response.Response({
                "you are": "a rendi"
            })
        
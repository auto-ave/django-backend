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
                "name": "{} {}".format(user.first_name, user.last_name),
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

    def post(self, request):
        # data = self.validate(request)
        data = request.data

        checksum = ""
        form = data

        response_dict = {}

        for i in form.keys():
            response_dict[i] = form[i]
            if i == 'CHECKSUMHASH':
                # 'CHECKSUMHASH' is coming from paytm and we will assign it to checksum variable to verify our paymant
                checksum = form[i]

            if i == 'ORDERID':
                # we will get an order with id==ORDERID to turn isPaid=True when payment is successful
                print('paytm ki ma ki chut')

        # we will verify the payment using our merchant key and the checksum that we are getting from Paytm request.POST
        verify = PaytmChecksum.verifySignature(response_dict, settings.PAYTM_MKEY, checksum)

        if True:
            if response_dict['RESPCODE'] == '01':
                booking = Booking.objects.get(booking_id=form.get('ORDERID'))
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
                # if the response code is 01 that means our transaction is successfull
                print('order successful')
                # after successfull payment we will make isPaid=True and will save the order
                booking.status = 1
                booking.save()
                # we will render a template to display the payment status
                return response.Response(response_dict)
            else:
                print('order was not successful because' + response_dict['RESPMSG'])

                return response.Response(response_dict)
        else:
            print('checksum verification failed')
            return response.Response({
                "you are": "a rendi"
            })
        
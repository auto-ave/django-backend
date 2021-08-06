from rest_framework import generics
from django.http import HttpResponse

from booking.models import *
from booking.serializers.general import *

from common.permissions import IsConsumer

from paytmchecksum import PaytmChecksum
import json, requests

from django.conf import settings

class BookingsList(generics.ListAPIView):
    serializer_class = BookingListSerializer
    permission_classes = ( IsConsumer, )

    def get_queryset(self):
        return self.request.user.consumer.bookings.all()

class BookingDetail(generics.RetrieveAPIView):
    lookup_field = 'booking_id'
    serializer_class = BookingDetailSerializer
    permission_classes = ( IsConsumer, )

    def get_queryset(self):
        return self.request.user.consumer.bookings.all()

def Paytm(request):
    # initialize an Hash/Array
    paytmParams = {}

    paytmParams["MID"] = "erKfbl49402655016816"
    paytmParams["ORDERID"] = "YOUR_ORDER_ID_HERE"

    # Generate checksum by parameters we have
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
    paytmChecksum = PaytmChecksum.generateSignature(paytmParams, "y1RPZDGVbo0ySQ2S")
    print("generateSignature Returns:" + str(paytmChecksum))
    return HttpResponse("<h1>Paytm</h1>")

    paytmParams = dict()
    paytmParams = request.form.to_dict()
    paytmChecksum = paytmChecksum
    paytmChecksum = paytmParams['CHECKSUMHASH']
    paytmParams.pop('CHECKSUMHASH', None)

    # Verify checksum
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    isVerifySignature = PaytmChecksum.verifySignature(paytmParams, "YOUR_MERCHANT_KEY",paytmChecksum)
    if isVerifySignature:
        print("Checksum Matched")
    else:
        print("Checksum Mismatched")

def initiateTransaction(request):

    

    return HttpResponse("<h1>Paytm fuck you</h1>")

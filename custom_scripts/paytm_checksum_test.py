import requests
import json

from paytmchecksum import PaytmChecksum

# Generate Checksum via Hash/Array
# initialize an Hash/Array
paytmParams = {}

paytmParams["MID"] = "XjcrPx92242589915926"
paytmParams["ORDERID"] = "D3FC3E4602"

# Generate checksum by parameters we have
# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
# paytmChecksum = PaytmChecksum.generateSignature(paytmParams, "3Gpkl1mfZgd82Wwi")
paytmChecksum = "5ImfD/dzbILZvbewPpQVy5WmyOZImPuayOUF+/GyA5I0CNOWTwchvInsEekbJ9S1FRNW6guuu2mEJkJ8RIYdjxsy5kgPunzfl05DhBWLZuQ="
verifyChecksum = PaytmChecksum.verifySignature(paytmParams, "3Gpkl1mfZgd82Wwi",paytmChecksum)

print("generateSignature Returns:" + str(paytmChecksum))
print("verifySignature Returns:" + str(verifyChecksum))

# Generate Checksum via String
# initialize JSON String
body = "{\"mid\":\"XjcrPx92242589915926\",\"orderId\":\"D3FC3E4602\"}"

# Generate checksum by parameters we have
# Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
# paytmChecksum = PaytmChecksum.generateSignature(body, "3Gpkl1mfZgd82Wwi")
paytmChecksum = "5ImfD/dzbILZvbewPpQVy5WmyOZImPuayOUF+/GyA5I0CNOWTwchvInsEekbJ9S1FRNW6guuu2mEJkJ8RIYdjxsy5kgPunzfl05DhBWLZuQ="
verifyChecksum = PaytmChecksum.verifySignature(body, "3Gpkl1mfZgd82Wwi", paytmChecksum)

print("generateSignature Returns:" + str(paytmChecksum))
print("verifySignature Returns:" + str(verifyChecksum))
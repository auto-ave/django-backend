import requests, json

PHONE_ID = "20341"
PRODUCT_ID = "b2a75f2f-2863-4e33-a887-92579ff677a9"
TOKEN_ID = "ebc51b05-3066-4fdb-8058-9ae20ef52444"

INSTANCE_URL = "https://api.maytapi.com/api"
    
def create_group(title, numbers):
    url = INSTANCE_URL + "/" + PRODUCT_ID + "/" + PHONE_ID + "/createGroup"
    payload = json.dumps({
        "name": title,
        "numbers": numbers
    })
    headers = {
        "Content-Type": "application/json",
        "x-maytapi-key": TOKEN_ID,
    }
    r = requests.post(url, headers=headers, data=payload)
    tjson = r.json()
    print('create group response: ', tjson)
    pSuccess = tjson["success"]
    if pSuccess == True:
        print('create group success')
    else:
        print('create group failed')
        
create_group("Test group with Subodh", ["+918989820993"])
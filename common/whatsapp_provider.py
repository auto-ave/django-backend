import requests, json
from background_task import background

PHONE_ID = "20341"
PRODUCT_ID = "b2a75f2f-2863-4e33-a887-92579ff677a9"
TOKEN_ID = "ebc51b05-3066-4fdb-8058-9ae20ef52444"

INSTANCE_URL = "https://api.maytapi.com/api"

class WhatsappProvider:
    def __init__(self, driver):
        self.driver = driver
    
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
            print('create group success\n')
            return tjson["data"]["id"]
        else:
            print('create group failed\n')
            return False
    
    @background(schedule=0)
    def change_group_profile_picture(group_id, picture_url):
        url = INSTANCE_URL + "/" + PRODUCT_ID + "/" + PHONE_ID + "/setProfileImage"
        payload = json.dumps({
            "conversation_id": group_id,
            "image": picture_url
        })
        headers = {
            "Content-Type": "application/json",
            "x-maytapi-key": TOKEN_ID,
        }
        r = requests.post(url, headers=headers, data=payload)
        tjson = r.json()
        print('profile picture change response: ', tjson)
        pSuccess = tjson["success"]
        if pSuccess == True:
            print('change profile picture success\n')
            return True
        else:
            print('change profile picture failed\n')
            return False
    
    @background(schedule=0)
    def add_participants_to_group(group_id, number):
        url = INSTANCE_URL + "/" + PRODUCT_ID + "/" + PHONE_ID + "/group/add"
        payload = json.dumps({
            "conversation_id": group_id,
            "number": number
        })
        headers = {
            "Content-Type": "application/json",
            "x-maytapi-key": TOKEN_ID,
        }
        r = requests.post(url, headers=headers, data=payload)
        tjson = r.json()
        print('add participant response: ', tjson)
        pSuccess = tjson["success"]
        if pSuccess == True:
            print('add participant success\n')
            return True
        else:
            print('add participant failed\n')
            return False
    
    @background(schedule=0)
    def send_text_message(number, message):
        url = INSTANCE_URL + "/" + PRODUCT_ID + "/" + PHONE_ID + "/sendMessage"
        payload = json.dumps({
            "to_number": number,
            "type": "text",
            "message": message
        })
        headers = {
            "Content-Type": "application/json",
            "x-maytapi-key": TOKEN_ID,
        }
        r = requests.post(url, headers=headers, data=payload)
        tjson = r.json()
        print('send message response: ', tjson)
        pSuccess = tjson["success"]
        if pSuccess == True:
            print('send message success\n')
            return True
        else:
            print('send message failed\n')
            return False
from accounts.models import User
from django.conf import settings
from background_task import background

from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

from misc.models import ErrorLogging
import requests

def OTP_MESSAGE(otp):
    return '{} is your OTP (One Time Password) to authenticate your login to Autoave'.format(otp)

class CommunicationProvider:

    @background(schedule=0)
    def send_email(email, subject="", html_content="", dynamic_template_data=None, template_id=None):
        sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)

        message = Mail(
            from_email= (settings.SENDGRID_SENDER, 'Autoave'),
            to_emails=email,
            subject=subject,
            html_content=html_content
        )
        
        if template_id and dynamic_template_data:
            message.template_id = template_id
            message.dynamic_template_data = dynamic_template_data
        
        print(message.get())
        response = sendgrid_client.send(message)
        print("sendgrid response status code: ", response.status_code)
        print(response.body)
    
    @background(schedule=0)
    def send_sms(numbers, message_id, variables_values=""):
        SENDER_ID = "AUTAVE"
        ROUTE = "dlt"
        url = "https://www.fast2sms.com/dev/bulkV2"
        
        payload = "sender_id={}&message={}&variables_values={}&route={}&numbers={}".format(
            SENDER_ID, message_id, variables_values, ROUTE, numbers
        )
        headers = {
            'authorization': settings.FAST2SMS_API_KEY,
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
         }
        response = requests.post(
            url,
            data=payload,
            headers=headers
        )
        print(response.text)
    
    
    
    @background(schedule=0)
    def send_otp(self, otp, number):
        sms_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = OTP_MESSAGE(otp)
        response = sms_client.messages.create(
            to=number,
            from_=settings.TWILIO_NUMBER,
            body=message
        )
        return response
    
    @background(schedule=0)
    def send_notification(userid, title, body, image="", data={}, topic=None):
        user = User.objects.get(id=userid)
        devices = user.get_devices()
        if devices:
            notification = Notification(title=title, body=body, image=image)
            message = Message(
                notification=notification,
                data=data,
                topic=topic,
            )
            result = devices.send_message(message)
            # print('notification result: ', str(result))
            # print('list: ', str(result[0].responses))
            # print('first object: ', str(result[0].responses[0]))
            # print('exception: ', str(result[0].responses[0].exception))
            # print('messag id: ', str(result[0].responses[0].message_id))
            # print('succes boolean: ', str(result[0].responses[0].success))

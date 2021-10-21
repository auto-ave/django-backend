

from accounts.models import User
from django.conf import settings
from background_task import background

from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

def OTP_MESSAGE(otp):
    return '{} is your OTP (One Time Password) to authenticate your login to Autoave'.format(otp)

class CommunicationProvider:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)

    def send_sms(self, number, message):

        response = self.client.messages.create(
            to=number,
            from_=settings.TWILIO_NUMBER,
            body=message)

        return response

    def send_email(self, email, subject, html_content):
        message = Mail(
            from_email= settings.SENDGRID_SENDER,
            to_emails=email,
            subject=subject,
            html_content=html_content)

        response = self.sendgrid_client.send(message)
        return response
    
    def send_otp(self, otp, number):
        message = OTP_MESSAGE(otp)
        response = self.send_sms(number=number, message=message)
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
            devices.send_message(message)

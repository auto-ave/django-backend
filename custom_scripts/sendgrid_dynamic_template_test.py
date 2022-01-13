from booking.models import *
from django.conf import settings
from common.utils import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

booking = Booking.objects.first()
store = booking.store
event = booking.event
vehicle_model = booking.vehicle_model
user = booking.booked_by.user

dynamic_template_data =  {
        # "email": list(filter( None, [store.owner.user.email, store.email] )),
        # "template_id": "d-28d7bcd7d3854ec8ae3bf9b4aa2be5fd",
        "booking_id": str(booking.booking_id),
            "store_name": str(store.name),
            "vehicle": {
                "brand": str(vehicle_model.brand.name),
                "model": str(vehicle_model.model),
            },
            "slot": {
                "start_time": event.start_datetime.strftime('%d %b - %I:%M %p'),
                "end_time": event.end_datetime.strftime('%d %b - %I:%M %p'),
                "duration": int(dateTimeDiffInMinutes(event.end_datetime, event.start_datetime)),
                "date": event.start_datetime.strftime('%d %b'),
            },
            "remaining_amount": float(booking.amount) - float(booking.payment.amount),
            "services": [ str(item.service.name) for item in booking.price_times.all() ],
            "customer": {
                "name": str(user.full_name()),
                "phone": str(user.phone),
                "email": str(user.email)
            }
    }

sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)

message = Mail(
    from_email= settings.SENDGRID_SENDER,
    to_emails='vermasubodhk@gmail.com',
    subject='hello wrold',
    html_content='adfasdf'
)

message.template_id = "d-28d7bcd7d3854ec8ae3bf9b4aa2be5fd"
message.dynamic_template_data = dynamic_template_data

response = sendgrid_client.send(message)
print("sendgrid response status code: ", response.status_code)
print(response.body)
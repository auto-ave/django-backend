from rest_framework.serializers import ValidationError
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python

class CustomPhoneNumberField(PhoneNumberField):
    def to_internal_value(self, data):
        phone_number = to_python(data)
        if phone_number and not phone_number.is_valid():
            raise ValidationError(self.error_messages["invalid"])
        return phone_number.as_e164
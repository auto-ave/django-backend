def clean_phone_number(phone_number):
    """
    Cleans a phone number string.
    """
    if len(phone_number) == 10:
        return "91" + phone_number
    
    return "91" + phone_number.replace(' ', '').replace('-', '').replace(')', '').replace('(', '').strip('+').lstrip('0').lstrip('91').lstrip('0')
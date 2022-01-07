def SMS_LOGIN_CONTENT(phone, otp):
    # return {
    #     "data": {
    #         "route" : "dlt",
    #         "sender_id" : "AUTAVE",
    #         "message" : "135722",
    #         "variables_values" : "{}|".format(str(otp)),
    #         "flash" : 1,
    #         "numbers" : str(phone),
    #     }
    # }
    return {
        'message_id': '135722',
        'variables_values': '{}|'.format(str(otp)),
        'numbers': str(phone),
    }
from rest_framework.views import exception_handler
import traceback as tb

from misc.models import ErrorLogging

FAIL_MESSAGE = "Unknown error occurred"

class StatusCode():
    SUCCESS = 'success'
    FAIL = 'fail'
    ERROR = 'error'

class ResponseData():
    def __init__(self, status, message, data={}):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            'status': self.status,
            'message': self.message,
            'data': self.data
        }

def autoave_exception_handler(exception, context):
    response = exception_handler(exception, context)
    if response is not None:
        response.data = ResponseData(
            StatusCode.ERROR,
            FAIL_MESSAGE,
            response.data
        ).to_dict()
    else:
        ErrorLogging.objects.create(
            context=str(context),
            exception=str(exception),
            traceback=tb.format_exc()
        )
    return response

    
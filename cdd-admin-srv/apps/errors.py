from django.utils.encoding import force_text

from rest_framework import status
from rest_framework.exceptions import APIException


class ServerError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None):
        if code:
            self.code = code
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.default_detail)


def raise_server_error(message, code=None):
    raise ServerError(detail=message, code=code)


ERROR_CODE_SUCCESS = 0
ERROR_CODE_INVALID_PARAMS = 100
ERROR_CODE_INVALID_ACTION = 101

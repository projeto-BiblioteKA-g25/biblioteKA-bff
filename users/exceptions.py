from rest_framework.exceptions import APIException


class NotFollowBookError(APIException):
    status_code = 404

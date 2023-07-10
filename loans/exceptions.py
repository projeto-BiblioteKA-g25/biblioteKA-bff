from rest_framework.exceptions import APIException


class SuspendedUserError(APIException):
    status_code = 403


class CopyUnavailableError(APIException):
    status_code = 404


class UserIsBlockedError(APIException):
    status_code = 403


class LoanAlreadyReturnError(APIException):
    status_code = 403

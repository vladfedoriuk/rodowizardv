from collections import namedtuple
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


StatusCode = namedtuple("StatusCode", ["code", "text"])
ResponseData = namedtuple("ResponseData", ["http_status", "errors", "message", "data"])

CODE_200 = StatusCode(200, _("OK"))
CODE_404 = StatusCode(404, _("Item was not found"))
CODE_403 = StatusCode(403, _("You have no access."))
CODE_400 = StatusCode(400, _("The provided data are invalid"))


class WrongPersonalDataUUID(APIException):
    status_code = 400
    default_detail = _("The uuid of the personal data is invalid.")
    default_code = "wrong_personal_data_id"

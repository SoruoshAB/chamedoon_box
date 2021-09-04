from rest_framework.views import APIView
from django.http import HttpRequest

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from accounts.soapAPI import soapapi
from accounts.util import Util_Accounts
from chamedoon.util import util


class SendCodeToPhoneNumber(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request: HttpRequest):
        phone_number = str(request.data['phone_number'])
        if not Util_Accounts.is_phone_number_valid(phone_number):
            return util.response_generator("phone number is invalid", 406, {})

        code = soapapi.send_verification_code_to_phone_number(phone_number)

        store_result = Util_Accounts().store_string_redis(key=phone_number, string=str(code),
                                                          expire=Util_Accounts().verification_code_expire_time)

        if not store_result:
            return util.response_generator("error in save phone number", 500, {})

        return util.response_generator("ok", 200, "SEND SMS")

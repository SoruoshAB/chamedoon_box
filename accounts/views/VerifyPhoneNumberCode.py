from datetime import datetime, timedelta

from rest_framework.views import APIView
from django.http import HttpRequest

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from chamedoon.util import util

from accounts.util import Util_Accounts

from accounts.util_api import UtilApi


class VerifyPhoneNumberCodeApp(APIView):
    @method_decorator(csrf_exempt)
    def put(self, request: HttpRequest):
        code = str(request.data['code'])
        phone_number = str(request.data['phone_number'])
        android_version = int(request.data['android_version'])
        device_type = str(request.data['device_type'])
        device_unique_id = str(request.data['unique_id'])
        device_fcm_token = str(request.data['fcm_token'])

        if not Util_Accounts.is_verification_code_valid(code):
            return util.response_generator("verification code is invalid", 406, {})

        check_result = Util_Accounts().checkVerificationCode(key=phone_number, code=code)

        if not check_result:
            return util.response_generator("verification code has been expired", 406, {})

        try:
            user_id, device = UtilApi.send_data_new_user(phone_number, android_version, device_type,
                                                         device_unique_id, device_fcm_token)
            if user_id or device:
                new_refresh_token = Util_Accounts().generate_refresh_token(datetime.utcnow() + timedelta(days=5),
                                                                           device=device,
                                                                           user_id=user_id)
                new_access_token = Util_Accounts().generate_access_token(datetime.utcnow() + timedelta(days=3),
                                                                         device=device,
                                                                         user_id=user_id,
                                                                         refresh_token=new_refresh_token.decode("utf8"))
                return util.response_generator(msg="ok", status_code=200, data={"access_token": new_access_token,
                                                                                "refresh_token": new_refresh_token})
            else:
                return util.response_generator("The internet is weak. Try another time", 408, {})
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})

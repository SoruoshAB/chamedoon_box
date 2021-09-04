from datetime import datetime, timedelta

import jwt
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from accounts.util import Util_Accounts
from chamedoon.util import util


class RefreshJwtToken(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request: HttpRequest):

        refresh_token = str(request.data['refresh_token'])

        if 'Authorization' not in request.headers:
            return util.response_generator(msg="authentication faild", status_code=403, data={})

        access_token = str(request.headers['Authorization'])
        access_token_content = jwt.decode(jwt=access_token, key=Util_Accounts().get_jwt_secret_key(),
                                          algorithms="HS256", options={'verify_exp': False})

        if not Util_Accounts.is_jwt_access_token_content_valid(access_token_content):
            return util.response_generator(msg="authentication faild", status_code=403, data={})

        refresh_token_content = jwt.decode(jwt=refresh_token, key=Util_Accounts().get_jwt_secret_key(),
                                           algorithms="HS256")

        if not Util_Accounts.is_jwt_refresh_token_content_valid(refresh_token_content):
            return util.response_generator(msg="invalid refresh token", status_code=403, data={})

        if refresh_token != access_token_content["refresh_token"]:
            return util.response_generator(msg="invalid refresh token", status_code=403, data={})

        if access_token_content["device"] == "android" or access_token_content["device"] == "ios":
            new_refresh_token = Util_Accounts().generate_refresh_token(datetime.utcnow() + timedelta(days=100),
                                                                       device=access_token_content["device"],
                                                                       user_id=access_token_content["user_id"])
            new_access_token = Util_Accounts().generate_access_token(datetime.utcnow() + timedelta(days=30),
                                                                     device=access_token_content["device"],
                                                                     user_id=access_token_content["user_id"],
                                                                     refresh_token=new_refresh_token)

        else:  # if access_token_content["device"] == "web"
            new_refresh_token = Util_Accounts().generate_refresh_token(datetime.utcnow() + timedelta(days=5),
                                                                       device=access_token_content["device"],
                                                                       user_id=access_token_content["user_id"])
            new_access_token = Util_Accounts().generate_access_token(datetime.utcnow() + timedelta(days=1),
                                                                     device=access_token_content["device"],
                                                                     user_id=access_token_content["user_id"],
                                                                     refresh_token=new_refresh_token)

        return util.response_generator(msg="ok", status_code=200, data={"access_token": new_access_token,
                                                                        "refresh_token": new_refresh_token})

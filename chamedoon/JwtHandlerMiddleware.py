from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest
from django.conf import settings
from django.http import HttpResponse
import json
import os
import jwt

jwt_secret_key_file_name = "jwt_secret_key.txt"
white_list = ["/api/accounte/SendCodeToPhoneNumber",
              "/api/accounte/VerifyPhoneNumberCodeApp",
              "/api/accounte/RefreshJwtToken",
              ]


class JwtHandler(MiddlewareMixin):

    def is_jwt_access_token_content_valid(self, jwt_content):
        if ("exp" not in jwt_content.keys() or
                "user_id" not in jwt_content.keys() or
                "device" not in jwt_content.keys() or
                "refresh_token" not in jwt_content.keys()):
            return False
        return True

    def is_jwt_refresh_token_content_valid(self, jwt_content):
        if ("exp" not in jwt_content.keys() or
                "user_id" not in jwt_content.keys() or
                "device" not in jwt_content.keys()):
            return False
        return True

    def getJwtSecretKey(self):
        key = ""
        with open(os.path.dirname(os.path.dirname(__file__)) + os.path.sep + jwt_secret_key_file_name, "r") as lines:
            for line in lines:
                key = key + line
        return key

    def response_generator(self, msg: str, status_code: int, data):
        js = {'message': msg, 'data': data}
        response = HttpResponse(json.dumps(js),
                                content_type="application/json",
                                status=status_code)  # Response(js, status=status_code)
        return response

    def process_view(self, request: HttpRequest, view_function, view_args, view_kwargs):

        if (request.path.__contains__("/api/docs/") or request.path.__contains__("/api/docs")) and settings.DEBUG:
            return None

        if request.path.startswith("/api/admin") and settings.DEBUG:
            return None

        if request.path.startswith("/api/web"):
            return None

        if request.path.startswith("/api/set"):
            return None

        if white_list.__contains__(request.path):
            return None

        if 'AUTHORIZATION' in request.headers.keys():

            try:
                auth_content = jwt.decode(jwt=request.headers['Authorization'], key=self.getJwtSecretKey(),
                                          algorithms="HS256")
            except jwt.DecodeError as decodeError:
                return self.response_generator(msg="authentication faild", status_code=401, data={})
            except jwt.ExpiredSignatureError as expireError:
                if view_function.__name__ != "RefreshJwtToken" or "refresh_token" not in request.POST.keys():
                    return self.response_generator(msg="authentication faild", status_code=401, data={})
                else:
                    try:
                        auth_content = jwt.decode(jwt=request.headers['Authorization'], key=self.getJwtSecretKey(),
                                                  algorithms="HS256", options={'verify_exp': False})
                        return None
                    except jwt.DecodeError:
                        return self.response_generator(msg="authentication faild", status_code=401, data={})

            if not self.is_jwt_access_token_content_valid(auth_content):
                return self.response_generator(msg="authentication faild", status_code=401, data={})
        else:
            return self.response_generator(msg="authentication faild", status_code=401, data={})

        return None

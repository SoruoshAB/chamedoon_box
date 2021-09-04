import os
import re
from random import randint

import jwt
from redis import Redis

from accounts.soapAPI import soapapi


class Util_Accounts:
    def __init__(self):
        self.redis = Redis(host='box_redis', port=6379)
        self.username_valid_ascii_codes = [46,  # dot
                                           95,  # underscore
                                           ]
        self.verification_code_expire_time = 120
        self.jwt_secret_key_file_name = "jwt_secret_key.txt"
        self.datetime_format = "%Y/%m/%d-%H:%M:%S"

    @staticmethod
    def is_phone_number_valid(phone_number: str) -> bool:
        regex_phone = '(\+98|0)?(3|9)\d{9}'
        if bool(re.search(regex_phone, phone_number)):
            return True

    @staticmethod
    def send_verification_code_to_phone_number(phone_number: str = '09136025944'):
        code = randint(100000, 999999)
        msa = str("کد اعتبار سنجی شما در چمدون: " + "\n " + str(code))
        soa = soapapi('sorushi', 'Sa129/5890*do')
        res = soa.SendMessageWithCode('09136025944', code)
        return code

    def store_string_redis(self, key: str, string: str, expire: int = -1):
        if expire != -1:
            result = self.redis.set(name=key, value=string, ex=expire)
        else:
            result = self.redis.set(name=key, value=string)
        return result

    @staticmethod
    def is_verification_code_valid(code: str):
        if len(code) != 6:
            return False
        return True

    def checkVerificationCode(self, key: str, code: str):
        stored_code = self.redis.get(key)
        if not stored_code:
            return False
        return stored_code.decode("utf8") == code

    def get_jwt_secret_key(self):
        key = ""
        with open(os.path.dirname(os.path.dirname(__file__)) + os.path.sep + self.jwt_secret_key_file_name,
                  "r") as lines:
            for line in lines:
                key = key + line
        return key

    def generate_refresh_token(self, expire_time, device, user_id):
        payload = {"exp": expire_time, "device": device, "user_id": user_id}
        refresh_token = jwt.encode(payload=payload, key=self.get_jwt_secret_key())
        return refresh_token

    def generate_access_token(self, expire_time, device, user_id, refresh_token: str):
        payload = {"exp": expire_time, "device": device, "user_id": user_id, "refresh_token": refresh_token}
        access_token = jwt.encode(payload=payload, key=self.get_jwt_secret_key())
        return access_token

    @staticmethod
    def is_jwt_access_token_content_valid(jwt_content):
        if ("exp" not in jwt_content.keys() or
                "user_id" not in jwt_content.keys() or
                "device" not in jwt_content.keys() or
                "refresh_token" not in jwt_content.keys()):
            return False
        return True

    @staticmethod
    def is_jwt_refresh_token_content_valid(jwt_content):
        if ("exp" not in jwt_content.keys() or
                "user_id" not in jwt_content.keys() or
                "device" not in jwt_content.keys()):
            return False
        return True

import os
import random
import datetime

import jwt
from django.http import HttpRequest
from rest_framework.response import Response

from apiApp.models import Ads


class util:
    def __init__(self):
        self.jwt_secret_key_file_name = "jwt_secret_key.txt"

    @staticmethod
    def response_generator(msg: str, status_code: int, data):
        js = {'message': msg, 'data': data}
        response = Response(js, status=status_code)
        return response

    @staticmethod
    def get_an_ad():
        ads = list(Ads.objects.filter(is_video_ads=False))
        random.shuffle(ads)
        if ads.__len__() != 0:
            return [{"ad_id": ads[0].ad_id, "image_url": ads[0].image_url, "click_url": ads[0].click_url}, ]
        else:
            return []

    @staticmethod
    def get_three_ads():
        ads = list(Ads.objects.filter(is_video_ads=False, is_active=True))
        random.shuffle(ads)
        if ads.__len__() >= 3:
            return [{"ad_id": ads[0].ad_id, "image_url": ads[0].image_url, "click_url": ads[0].click_url},
                    {"ad_id": ads[1].ad_id, "image_url": ads[1].image_url, "click_url": ads[1].click_url},
                    {"ad_id": ads[2].ad_id, "image_url": ads[2].image_url, "click_url": ads[2].click_url}]
        else:
            return []

    @staticmethod
    def get_banners():
        try:
            ads = list(Ads.objects.select_related("video").filter(is_video_ads=True, is_active=True))
            random.shuffle(ads)
            if ads.__len__() >= 1:
                return {"video_id": ads[0].video.video_id, "image_url": ads[0].image_url, "slug": ads[0].video.slug}
            else:
                return {}
        except Exception as e:
            return [str(e)]

    @staticmethod
    def datetime_to_str(dt: datetime.datetime):
        if dt is not None:
            return dt.strftime("%Y/%m/%d-%H:%M:%S")
        else:
            return None

    def get_jwt_secret_key(self):
        key = ""
        with open(os.path.dirname(os.path.dirname(__file__)) + os.path.sep + self.jwt_secret_key_file_name,
                  "r") as lines:
            for line in lines:
                key = key + line
        return key

    @staticmethod
    def is_jwt_access_token_content_valid(jwt_content):
        if ("exp" not in jwt_content.keys() or
                "user_id" not in jwt_content.keys() or
                "device" not in jwt_content.keys() or
                "refresh_token" not in jwt_content.keys()):
            return False
        return True

    def get_user_id_from_access_token(self, request: HttpRequest):
        try:
            access_token = str(request.headers['Authorization'])
            access_token_content = jwt.decode(jwt=access_token, key=self.get_jwt_secret_key(),
                                              algorithms="HS256")
        except Exception as e:
            return None

        if not self.is_jwt_access_token_content_valid(access_token_content):
            return None

        return int(access_token_content['user_id'])

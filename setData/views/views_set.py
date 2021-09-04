import json
from datetime import datetime

import requests
from chamedoon.util import util
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from setData.set_data import SetData
from variables import variables

from setData.downloader import Downloader


class get_data(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            # http://37.152.182.80/api/box/get/data/1
            req = requests.request("GET", variables().api_get_data, timeout=1)
            if req.status_code == 200:
                data = req.json()['data']
                videos = data['video']
                songs = data['song']
                ads = data['ads']
                slider_home = data['slider_home']
                # if req.status_code == 200:
                #     company = data['company']
                video = SetData.set_video(videos)
                song = SetData.set_song(songs)
                ads = SetData.set_ads(ads)
                slider_home = SetData.set_slider_home(slider_home)
                downloader_data = video + song + ads + slider_home
                Downloader.send_2_downloader(downloader_data) if downloader_data else None
                return util.response_generator("ok", 200, data, )
            else:
                data = "api error"
                return util.response_generator("server error", 500, data, )
        except Exception as e:
            return util.response_generator("internal server error :", 500, {str(e)})


class verify_downloader(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request: HttpRequest):
        try:
            data = request.body.decode('utf-8')
            data = json.loads(data)
            status = data["status"]
            url = data['url']
            type = data['type']
            Downloader.verify_download(url, type) if status == 'DONE' else None
            return util.response_generator("ok", 200, data)
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " : Failed : " + str(e))
            f.close()
            return util.response_generator("internal server error", 500, [str(e)])


class test_downloader(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request: HttpRequest):
        try:
            data = request.data
            f = open("a.txt", "a+")
            f.write("\r\n " + str(data) + "\r\n " + str(datetime.utcnow()) + "\r\n")
            f.close()
            return util.response_generator("ok", 200, [])
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})

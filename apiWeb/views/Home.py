from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apiWeb.util import Util_Web
from chamedoon.util import util


class home_slider(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            result = {
                'slider_video': Util_Web.get_slider_video(True),
                'slider_song': Util_Web.get_slider_song(True),
                'slider_ads': Util_Web.get_slider_ads()
            }
            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class home_video(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_new_videos())
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class home_song(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_latest_songs())
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class home_podcast(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_latest_podcasts())
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class home_ads(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, util.get_three_ads())
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class search(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            search = request.query_params['q']
            return util.response_generator("ok", 200, Util_Web.search(search))
        except Exception as e:
            return util.response_generator("internal server error  :" + str(e), 500, {})

from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apiApp.util import Util_App
from chamedoon.util import util


class Home(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})

        try:
            result = {
                'slider': Util_App.get_home_slider(),
                'newest_video': Util_App.get_new_videos(),
                'newest_song': Util_App.get_new_songs(),
                'newest_podcast': Util_App.get_new_podcast(),
                'ads': util.get_three_ads()
            }

            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error", 500, {})


class child(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            result = {
                'slider': Util_App.get_slider_video_child(),
                'animations': Util_App.get_new_videos_child(),
                'animations_image': Util_App.get_new_videos_child(12, False),
                'song_child': Util_App.get_new_songs_child()
            }

            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error  :" + str(e), 500, {})


class search(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            search = request.query_params['search']
            return util.response_generator("ok", 200, Util_App.search(search))
        except Exception as e:
            return util.response_generator("internal server error  :" + str(e), 500, {})

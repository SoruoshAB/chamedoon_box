from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apiWeb.util import Util_Web
from chamedoon.util import util


class songs_slider(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_song_slider())
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class songs_latest(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_latest_songs())
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class songs_popular(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_popular_songs())
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class songs_podcasts_latest(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_latest_podcasts())
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class songs_podcasts_popular(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_popular_podcasts())
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class songs_playlists(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_song_playlists())
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class songs_all_playlists(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_all_playlists())
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class playlist_songs(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, playlist_id: int):
        try:
            result = Util_Web.get_playlist_songs(playlist_id)
            if result:
                return util.response_generator("ok", 200, result)
            else:
                return util.response_generator("Not Found", 404, "")
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class songs_singers(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_song_singers())
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class songs_all_singers(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_all_singers())
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class singer_songs(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, singer_id: int):
        try:
            result = Util_Web.get_singer_songs(singer_id)
            if result:
                return util.response_generator("ok", 200, result)
            else:
                return util.response_generator("Not Found", 404, "")
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class songs_channels(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            result = Util_Web.get_channels()
            if result:
                return util.response_generator("ok", 200, result)
            else:
                return util.response_generator("Not Found", 404, "")
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class songs_all_channel(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            result = Util_Web.get_channel_all()
            if result:
                return util.response_generator("ok", 200, result)
            else:
                return util.response_generator("Not Found", 404, "")
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class channel_songs(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, channel_id: int):
        try:
            result = Util_Web.get_channel_songs(channel_id)
            if result:
                return util.response_generator("ok", 200, result)
            else:
                return util.response_generator("Not Found", 404, "")
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class songs_ads(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, util.get_three_ads())
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])

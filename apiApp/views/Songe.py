from django.db.models import Prefetch
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

# from accounts.util import Util_Accounts
from apiApp.models.Song import *
from apiApp.util import Util_App
from chamedoon.util import util

from apiApp.models import Singer_Channel, Songs, Playlists

from apiApp.util_api import UtilApi


class Music(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            result = {
                'slider_song': Util_App.get_slider_song(),
                "play_list": Util_App.get_play_list(),
                "singer": Util_App.get_new_singer(),
                "newest_song": Util_App.get_new_songs(),
                "newest_channel": Util_App.get_new_channel(),
                "newest_podcast": Util_App.get_new_podcast(),
                'ads': util.get_three_ads(),
            }
            return util.response_generator("ok", 200, result)

        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class get_all_songs(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            songs = Util_App.get_all_popular_songs(page)
            result = {
                "page": page,
                "pages_count": songs[0],
                "songs": songs[1]
            }
            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class get_all_channel(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            channels = Util_App.get_all_channels(page)
            result = {
                "page": page,
                "pages_count": channels[0],
                "channels": channels[1]
            }
            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class get_all_podcast(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            podcasts = Util_App.get_all_podcasts(page)
            result = {
                "page": page,
                "pages_count": podcasts[0],
                "podcasts": podcasts[1]
            }
            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class get_all_singer(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            singer_data = Util_App.get_all_singer(page)
            result = {
                "page": page,
                "pages_count": singer_data[0],
                "single_song": singer_data[1]
            }
            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class get_singer_channel(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, singer_channel_id: int):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            prefetch1 = Prefetch("songs_set",
                                 queryset=Songs.objects.filter(is_active_link=True, is_active_image=True, ).order_by(
                                     '-singer_id'),
                                 to_attr="song_all"
                                 )
            prefetch2 = Prefetch("songs_set",
                                 queryset=Songs.objects.filter(is_active_link=True, is_active_image=True, ).order_by(
                                     '-view_count'),
                                 to_attr="song_all_popular"
                                 )
            singer_channel = Singer_Channel.objects.prefetch_related(prefetch1, prefetch2).filter(
                singer_id=singer_channel_id, is_active=True).first()
            if singer_channel:
                result = {
                    "singer_channel": dict(name=singer_channel.fa_name, image_link=singer_channel.image_link),
                    "popular_songs": Util_App.get_popular_songs_singer(singer_channel),
                    "playlist": Util_App.get_play_list(),
                    "single_song": Util_App.get_five_songs_singer(singer_channel),
                    'ads': util.get_three_ads(),
                }

                return util.response_generator("ok", 200, result)
            else:
                return util.response_generator("singer or channel not found", 404, {})
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class get_singer_channel_single_song(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, singer_channel_id: int, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            prefetch1 = Prefetch("songs_set",
                                 queryset=Songs.objects.filter(is_active_link=True,
                                                               is_active_image=True,
                                                               singer__is_active=True).order_by('-singer_id'),
                                 to_attr="song_all"
                                 )
            singer_channel = Singer_Channel.objects.prefetch_related(prefetch1).filter(singer_id=singer_channel_id,
                                                                                       is_active=True).first()
            if singer_channel:
                song_data = Util_App.get_all_songs_singer(singer_channel, page)
                result = {
                    "page": page,
                    "pages_count": song_data[0],
                    "single_song": song_data[1]
                }
                return util.response_generator("ok", 200, result)
            else:
                return util.response_generator("singer or channel not found", 404, {})
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class get_singer_channel_popular_song(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, singer_channel_id: int, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            prefetch = Prefetch("songs_set",
                                queryset=Songs.objects.filter(is_active_link=True, is_active_image=True, ).order_by(
                                    '-view_count'),
                                to_attr="song_all_popular"
                                )
            singer_channel = Singer_Channel.objects.prefetch_related(prefetch).filter(singer_id=singer_channel_id,
                                                                                      is_active=True).first()
            if singer_channel:
                popular_songs = Util_App.get_all_popular_songs_singer(singer_channel, page)
                result = {
                    "page": page,
                    "pages_count": popular_songs[0],
                    "single_song": popular_songs[1]
                }
                return util.response_generator("ok", 200, result)
            else:
                return util.response_generator("singer or channel not found", 404, {})
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class AddViewSongCount(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, song_id: int):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            song = Songs.objects.filter(song_id=song_id).first()
            if song:
                set_view = UtilApi.add_view_count_song(song_id, request.headers['Authorization'])
                if set_view:
                    song.view_count += 1
                    song.save()
                    return util.response_generator("ok", 200, {})
                else:
                    return util.response_generator("sever error", 500, {})
            else:
                return util.response_generator("video not found", 404, {})
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class get_playlist(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, playlist_id: int):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            prefetch1 = Prefetch("songs",
                                 queryset=Songs.objects.select_related("singer").filter(is_active_link=True,
                                                                                        is_active_image=True, ).order_by(
                                     '-singer_id'),
                                 to_attr="song_all"
                                 )
            prefetch2 = Prefetch("songs",
                                 queryset=Songs.objects.select_related("singer").filter(is_active_link=True,
                                                                                        is_active_image=True, ).order_by(
                                     '-view_count'),
                                 to_attr="song_all_popular"
                                 )
            Playlist = Playlists.objects.prefetch_related(prefetch1, prefetch2).filter(playlist_id=playlist_id,
                                                                                       is_active=True, ).first()
            if Playlist:
                single_song = Util_App.get_songs_playlist(Playlist)
                result = {
                    'playlist_data': {"name": Playlist.name, 'image': Playlist.cover},
                    'popular_song': Util_App.get_popular_songs_playlist(Playlist)[1],
                    'playlist': Util_App.get_play_list(),
                    'ads': util.get_three_ads(),
                    "pages_count": single_song[0],
                    'single_song': single_song[1]
                }

                return util.response_generator("ok", 200, result)
            else:
                return util.response_generator("playlist not found", 404, {})
        except Exception as e:
            return util.response_generator("internal server error :" + str(e), 500, [])


class get_single_songs_playlist(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, playlist_id: int, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            prefetch1 = Prefetch("songs",
                                 queryset=Songs.objects.select_related("singer").filter(is_active_link=True,
                                                                                        is_active_image=True, ).order_by(
                                     '-singer_id'),
                                 to_attr="song_all"
                                 )
            Playlist = Playlists.objects.prefetch_related(prefetch1).filter(playlist_id=playlist_id,
                                                                            is_active=True).first()
            if Playlist:
                single_song = Util_App.get_songs_playlist(Playlist, page)
                result = {
                    "page": page,
                    "pages_count": single_song[0],
                    "data": single_song[1],
                }
                return util.response_generator("ok", 200, result)
            else:
                return util.response_generator("playlist not found", 404, {})
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class get_popular_songs_playlist(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, playlist_id: int, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            prefetch2 = Prefetch("songs",
                                 queryset=Songs.objects.select_related("singer").filter(is_active_link=True,
                                                                                        is_active_image=True, ).order_by(
                                     '-view_count'),
                                 to_attr="song_all_popular"
                                 )
            Playlist = Playlists.objects.prefetch_related(prefetch2).filter(playlist_id=playlist_id,
                                                                            is_active=True).first()
            if Playlist:
                popular_song = Util_App.get_popular_songs_playlist(Playlist, page)
                result = {
                    "page": page,
                    "pages_count": popular_song[0],
                    "data": popular_song[1],
                }
                return util.response_generator("ok", 200, result)
            else:
                return util.response_generator("playlist not found", 404, {})
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])

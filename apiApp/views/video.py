from apiApp.models.video import *
from apiApp.util import Util_App
from apiApp.util_api import UtilApi
from chamedoon.util import util
from django.db.models import Prefetch
from django.http import HttpRequest

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView


class Movies(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})

        try:
            prefecth = Prefetch("videos_set",
                                queryset=Videos.objects.filter(is_active_image=True, is_active_link=True),
                                to_attr="all_videos")
            categorys = VideoCategory.objects.prefetch_related(prefecth).filter(is_active=True,
                                                                                videos__is_active_image=True,
                                                                                videos__is_active_link=True).distinct()
            videos = Videos.objects.filter(is_active_link=True, is_active_image=True,
                                           is_childish=False)
            res_category = {}
            category_data = {}
            cat_number = 1
            for cat in categorys:
                res_category[('category' + str(cat_number))] = Util_App.Get_category(cat)
                category_data[('category' + str(cat_number))] = map(lambda video: Util_App.get_video(video),
                                                                    cat.all_videos[:10])
                cat_number += 1
            result = {
                'slider': Util_App.get_slider_video(),
                'category': res_category,
                'newest_video': Util_App.get_new_videos(videos),
                'visited_videos': Util_App.get_most_visited_videos(videos),
                'category_data': category_data,
                'ads': util.get_three_ads(),
            }
            banner = util.get_banners()
            if banner:
                result['banner'] = banner
            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error : " + str(e), 500, {})


class Video(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, video_id: int):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})

        try:
            video = Videos.objects.filter(video_id=video_id, is_active_link=True,
                                          is_active_image=True).first()
            if not video:
                return util.response_generator("video not found", 404, {})
            prefetch = Prefetch("videos",
                                queryset=Videos.objects.filter(is_active_link=True, is_active_image=True).exclude(
                                    video_id=video_id),
                                to_attr="all_video")
            video_genres = VideoGenres.objects.prefetch_related(prefetch).filter(videos__video_id=video_id)
            videos = set()
            for genre in video_genres:
                videos.update(genre.all_video)
            similar_videos = list(map(lambda video: Util_App.get_video(video), videos))[:10]
            video_res = {
                "video_id": video.video_id,
                "fa_name": video.fa_name,
                "en_name": video.en_name,
                "image_link": video.image_link,
                "min_age": video.min_age,
                "description": video.description,
                "length": video.length,
                "imdb_rating": video.imdb_rating,
                "director": video.director,
                "country_product": video.country_product,
                "is_dubbed": video.is_dubbed,
                "summary": video.summary,
                "genres": map(lambda genre: dict(genre_id=genre.genre_id, name=genre.name), video_genres),
                "links": video.link,
                "preview_link": video.preview_link if video.is_active_preview else None,
            }

            result = {
                'video_data': video_res,
                'images': Util_App.get_image_video(video),
                'actors': Util_App.get_actors_video(video),
                'suggested_videos': similar_videos,
                'ads': util.get_three_ads(),
            }

            return util.response_generator("ok", 200, result)

        except Exception as e:
            return util.response_generator("internal server error==>", 500, str(e))


class video_comments(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, video_id: int, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            video = Videos.objects.filter(video_id=video_id).first()
            if not video:
                return util.response_generator("video not found", 404, {})
            comments = UtilApi.get_comment(video.video_id, page, request.headers['Authorization'])
            if not comments:
                return util.response_generator("The internet is weak. Try another time", 408, {})
            return util.response_generator("ok", 200, comments)

        except Exception as e:
            return util.response_generator("internal server error" + " /n " + str(e), 500, {})

    def post(self, request: HttpRequest):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            video_id = request.data['video_id']
            message = request.data['message']
            video = Videos.objects.filter(video_id=video_id).first()
            print("video:", video)
            if not video:
                return util.response_generator("video not found", 404, {})
            comments = UtilApi.post_new_comment(video_id, message, request.headers['Authorization'])
            if comments:
                return util.response_generator("ok", 200, comments)
            else:
                return util.response_generator("internal server error", 500, "Error")
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class VideoCommentLike(APIView):
    def post(self, request: HttpRequest):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            comment_id = int(request.data['comment_id'])
            like = bool(str(request.data['like']).lower() == "true")
            comments = UtilApi.post_like_comment(comment_id, like, request.headers['Authorization'])

            return util.response_generator("ok", 200, comments)
        except Exception as e:
            return util.response_generator("internal server error", 500, {})


class AddViewVideoCount(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, video_id: int):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})
        try:
            video = Videos.objects.filter(video_id=video_id).first()
            if video:
                set_view = UtilApi.add_view_count_video(video_id, request.headers['Authorization'])
                if set_view:
                    video.view_count += 1
                    video.save()
                    return util.response_generator("ok", 200, {})
                else:
                    return util.response_generator("sever error", 500, {})
            else:
                return util.response_generator("video not found", 404, {})
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class get_all_videos(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})

        try:
            All_videos = Util_App.get_all_videos(page)
            result = {
                "page": page,
                "pages_count": All_videos[1],
                "videos": All_videos[0]
            }
            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class get_videos_category(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, cat_id: int, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})

        try:
            cat = VideoCategory.objects.filter(category_id=cat_id, is_active=True, ).first()
            if cat:
                cat_videos = Util_App.get_videos_category(cat_id, page)
                result = {
                    'name': cat.title,
                    'image': cat.image_link,
                    "page": page,
                    "pages_count": cat_videos[1],
                    "cat_videos": cat_videos[0]
                }
            else:
                return util.response_generator("category not found", 401, {})
            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class get_videos_genre(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, genre_id: int, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})

        try:
            genre = VideoGenres.objects.filter(genre_id=genre_id).first()
            if not genre:
                return util.response_generator("genre not found", 404, {})
            genre_videos = Util_App.get_videos_genre(genre_id, page)
            result = {
                'name': genre.name,
                "page": page,
                "pages_count": genre_videos[1],
                "genre_videos": genre_videos[0]
            }
            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])


class get_videos_actor(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, actor_id: int, page: int = 1):
        user_id = util().get_user_id_from_access_token(request)
        if user_id is None:
            return util.response_generator("Authorization:not found", 401, {})

        try:
            actor = VideoActors.objects.filter(actor_id=actor_id, is_active=True).first()
            if actor:
                actor_videos = Util_App.get_videos_actor(actor_id, page)
                result = {
                    'name': actor.fa_name,
                    'image': actor.avatar,
                    "description": actor.description,
                    "page": page,
                    "pages_count": actor_videos[1],
                    "actor_videos": actor_videos[0]
                }
            else:
                return util.response_generator("actor not found", 401, {})
            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error " + str(e), 500, [])

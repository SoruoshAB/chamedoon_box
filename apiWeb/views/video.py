from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apiApp.models.video import *
from apiWeb.util import Util_Web
from chamedoon.util import util

from apiWeb.util_api import UtilApi


class movies_slider(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_slider_video())
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class movies_category(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            videos = Videos.objects.select_related('category').filter(is_active_link=True, is_active_image=True,
                                                                      category__is_active=True)
            res_category = []
            res_category_inserted = []
            for video in videos:
                if video.category.category_id in res_category_inserted:
                    continue
                cat = video.category
                res_category.append(Util_Web.Get_category(cat))
                res_category_inserted.append(cat.category_id)
            return util.response_generator("ok", 200, res_category)
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class movies_category_video(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, cat_id: int):
        try:
            cat = VideoCategory.objects.filter(category_id=cat_id, is_active=True).first()
            if cat:
                result = {
                    "cat_title": cat.title,
                    "videos": cat.videos_set.filter(category_id=cat_id, is_childish=False, is_active_image=True,
                                                    is_active_link=True).order_by("-view_count").values("video_id",
                                                                                                        "fa_name",
                                                                                                        "en_name",
                                                                                                        "slug",
                                                                                                        "description",
                                                                                                        "imdb_rating",
                                                                                                        "image_link",
                                                                                                        "link")[:10]
                }
                return util.response_generator("ok", 200, result)
            else:
                return util.response_generator("cat is not found", 404, {})
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class movies_new_video(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_new_videos())
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class movies_most_visited_video(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, Util_Web.get_most_visited_videos())
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class movies_ads(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            return util.response_generator("ok", 200, util.get_three_ads())
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class movies_video_ads(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest):
        try:
            util.get_banners()
            return util.response_generator("ok", 200, util.get_banners())
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})


class one_video(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request: HttpRequest, video_slug: str):
        try:
            prefetch = Prefetch("videos",
                                queryset=Videos.objects.filter(is_childish=False, is_active_image=True,
                                                               is_active_link=True),
                                to_attr="video_all")
            prefetch_video = Prefetch("videogenres_set",
                                      queryset=VideoGenres.objects.prefetch_related(prefetch),
                                      to_attr="genres")
            video = Videos.objects.prefetch_related(prefetch_video).filter(slug=video_slug).first()
            if not video:
                return util.response_generator("video not found", 404, {})
            result = []
            similar_videos = []
            similar_videos_inserted = []
            genres = video.genres
            for genre in genres:
                for genre_video in genre.video_all:
                    if genre_video.video_id == video.video_id or genre_video.video_id in similar_videos_inserted:
                        continue
                    similar_videos.append(Util_Web.get_video(genre_video))
                    similar_videos_inserted.append(genre_video.video_id)

            similar_videos_paginator = Paginator(similar_videos, 10)
            similar_videos_page1 = similar_videos_paginator.get_page(1).object_list

            comments_response = UtilApi.get_comment(video.video_id)

            result.append({
                "video_id": video.video_id,
                "fa_name": video.fa_name,
                "en_name": video.en_name,
                "slug": video.slug,
                "image_link": video.image_link,
                "min_age": video.min_age,
                "description": video.description,
                "length": video.length,
                "imdb_rating": video.imdb_rating,
                "director": video.director,
                "country_product": video.country_product,
                "is_dubbed": video.is_dubbed,
                "summary": video.summary,
                "genres": map(lambda genre: dict(genre_id=genre.genre_id, name=genre.name), video.genres),
                "links": video.link,
                "Preview_link": video.preview_link,
                "actors": video.videoactors_set.filter(is_active=True).values("actor_id", "fa_name", "en_name",
                                                                              "avatar"),
                "images": video.videoimages_set.filter(is_active=True).values("image_id", "link", "name",
                                                                              "is_sticker"),
                "similar_videos": similar_videos_page1,
                "ads": util.get_three_ads(),
                "comments": comments_response if comments_response else []
            })
            return util.response_generator("ok", 200, result)
        except Exception as e:
            return util.response_generator("internal server error", 500, {str(e)})

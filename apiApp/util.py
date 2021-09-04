import datetime

from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from redis import Redis

from apiWeb.models import *
from .models import *


class Util_App:

    @staticmethod
    def get_home_slider():
        slider = {
            "slider_video": Util_App.get_slider_video(True),
            "slider_song": Util_App.get_slider_song(True),
            "slider_ads": Util_App.get_home_slider_ads(),
        }
        return slider

    @staticmethod
    def get_slider_video(is_home: bool = False):
        try:
            slider_video = []
            if is_home:
                slider_video_items = SliderHome.objects.prefetch_related("VideoSlider__video").filter(
                    type=SliderType.video.value,
                    VideoSlider__is_active=True,
                    VideoSlider__video__is_active_link=True,
                    VideoSlider__video__is_active_image=True, )
                for slider_video_item in slider_video_items:
                    video_slider = slider_video_item.VideoSlider
                    if video_slider:
                        video = video_slider.video
                        slider_video.append(dict(video_id=video.video_id,
                                                 image=video_slider.image_link,
                                                 fa_name=video.fa_name,
                                                 en_name=video.en_name))
            else:
                video_sliders = SliderVideo.objects.select_related("video").filter(is_show=True,
                                                                                   is_childish=False,
                                                                                   is_active=True,
                                                                                   video__is_active_link=True,
                                                                                   video__is_active_image=True, )
                if video_sliders:
                    for video_slider in video_sliders:
                        video = video_slider.video
                        slider_video.append(dict(video_id=video.video_id,
                                                 image=video_slider.image_link,
                                                 fa_name=video.fa_name,
                                                 en_name=video.en_name))
            return slider_video
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_slider_video_child(is_home: bool = False):
        try:
            slider_video_child = []
            if is_home:
                slider_video_child_items = SliderHome.objects.prefetch_related("VideoSlider__video").filter(
                    type=SliderType.video_child.value,
                    VideoSlider__is_active=True,
                    VideoSlider__is_childish=True,
                    VideoSlider__video__is_active_link=True,
                )
                for slider_video_child_item in slider_video_child_items:
                    video_slider = slider_video_child_item.VideoSlider
                    if video_slider:
                        video = video_slider.video
                        images = list(VideoImages.objects.filter(video=video, is_sticker=False,
                                                                 is_active=True).order_by("image_id"))
                        if images.__len__() >= 3:
                            images = images[:3]
                            image = (dict(image_id=image.image_id,
                                          link=image.link) for image in images)
                            slider_video_child.append(dict(video_id=int(video.video_id),
                                                           image_link=str(video_slider.image_link),
                                                           fa_name=str(video.fa_name),
                                                           des=str(video.description),
                                                           link=str(video.link),
                                                           images=image))
                return slider_video_child
            else:
                video_sliders = SliderVideo.objects.filter(is_show=True,
                                                           is_childish=True,
                                                           video__is_active_link=True,
                                                           is_active=True, )
                if video_sliders:
                    for video_slider in video_sliders:
                        video = video_slider.video
                        images = list(VideoImages.objects.filter(video=video, is_sticker=False,
                                                                 is_active=True).order_by("-image_id"))
                        if images.__len__() >= 3:
                            images = images[:3]
                            image = list(map(lambda image: dict(image_id=image.image_id,
                                                                link=image.link), images
                                             ))
                            slider_video_child.append(dict(video_id=int(video.video_id),
                                                           image_link=str(video_slider.image_link),
                                                           fa_name=str(video.fa_name),
                                                           description=str(video.description),
                                                           link=str(video.link),
                                                           images=image))
            return slider_video_child
        except:
            return []

    @staticmethod
    def get_video(video: Videos):
        home_video = {"video_id": int(video.video_id),
                      "fa_name": str(video.fa_name),
                      "en_name": str(video.en_name),
                      "image_link": str(video.image_link)}
        return home_video

    @staticmethod
    def get_new_videos(videos: Videos = None):
        if not videos:
            videos = Videos.objects.filter(is_childish=False, is_active_link=True,
                                           is_active_image=True).distinct().order_by('-video_id')
        home_videos = map(lambda video: Util_App.get_video(video), videos[:10]) if videos else []
        return home_videos

    @staticmethod
    def get_most_visited_videos(videos: Videos = None):
        if not videos:
            videos = Videos.objects.filter(is_childish=False, is_active_link=True, is_active_image=True).order_by(
                '-view_count')
        else:
            videos = videos.order_by('-view_count')
        home_videos = map(lambda video: Util_App.get_video(video), videos[:10]) if videos else []
        return home_videos

    @staticmethod
    def get_all_videos(page: int = 1):
        try:
            data_page = 0
            All_videos = []
            videos = Videos.objects.filter(is_childish=False, is_active_link=True, is_active_image=True) \
                .order_by('-view_count')
            if videos:
                videos_Paginator = Paginator(videos, 10)
                videos_page = videos_Paginator.get_page(page)
                data_page = videos_Paginator.num_pages
                All_videos = [Util_App.get_video(video) for video in videos_page]
            return All_videos, data_page
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_videos_category(cat_id: int, page: int = 1, videos: Videos = None):
        try:
            home_videos = []
            data_page = 0
            if not videos:
                videos = Videos.objects.filter(category_id=cat_id, is_active_link=True, is_active_image=True) \
                    .order_by("-view_count")
            else:
                videos = videos.filter(category_id=cat_id).order_by("-view_count")
            if videos:
                videos_Paginator = Paginator(videos, 10)
                videos_page = videos_Paginator.get_page(page)
                data_page = videos_Paginator.num_pages
                home_videos = [Util_App.get_video(video) for video in videos_page]
            return home_videos, data_page
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_video_child(video: Videos, image: bool = True):
        home_video = {"video_id": int(video.video_id),
                      "fa_name": str(video.fa_name),
                      "image_link": str(video.image_link),
                      "link": str(video.link)}
        if not image:
            del home_video["fa_name"]
        return home_video

    @staticmethod
    def get_new_videos_child(count_video: int = 21, image: bool = True):
        videos = Videos.objects.filter(is_childish=True, is_active_link=True, is_active_image=True) \
                     .order_by('-video_id')[:count_video]
        # home_videos = map(lambda video: Util_App.get_video_child(video), videos)
        if image:
            home_videos = map(lambda video: Util_App.get_video_child(video), videos)
        else:
            home_videos = map(lambda video: Util_App.get_video_child(video, image), videos)
        return home_videos

    @staticmethod
    def get_genres_video(video: Videos):
        try:
            genres_queryset = VideoGenres.objects.filter(videos__in=[video])
            genres = [dict(genre_id=genre.genre_id, name=genre.name) for genre in genres_queryset]

            return genres
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_videos_genre(genre_id: int, page: int = 1):
        try:
            videos_genre = []
            data_page = 0
            videos = Videos.objects.filter(videogenres__genre_id=genre_id, is_active_link=True,
                                           is_active_image=True).distinct().order_by("-view_count")
            if videos:
                videos_Paginator = Paginator(videos, 10)
                videos_page = videos_Paginator.get_page(page)
                data_page = videos_Paginator.num_pages
                videos_genre = [Util_App.get_video(video) for video in videos_page]
            return videos_genre, data_page
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_image_video(video: Videos):
        try:
            video_image = VideoImages.objects.filter(video=video, is_active=True).order_by('image_id')
            image_video = map(lambda image: dict(image_id=image.image_id,
                                                 link=image.link,
                                                 name=image.name,
                                                 is_sticker=image.is_sticker), video_image) if video_image else []
            return image_video
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_actors_video(video: Videos):
        try:
            actors_queryset = VideoActors.objects.filter(videos__in=[video], is_active=True)
            actors = map(lambda actor: dict(actor_id=actor.actor_id,
                                            fa_name=actor.fa_name,
                                            avatar=actor.avatar), actors_queryset) if actors_queryset else []
            return actors
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_videos_actor(actor_id: int, page: int = 1):
        try:
            videos_actor = []
            data_page = 0
            videos = Videos.objects.filter(videoactors__actor_id=actor_id, is_active_link=True, is_active_image=True) \
                .distinct().order_by("-view_count")
            if videos:
                videos_Paginator = Paginator(videos, 10)
                videos_page = videos_Paginator.get_page(page)
                data_page = videos_Paginator.num_pages
                videos_actor = [Util_App.get_video(video) for video in videos_page]
            return videos_actor, data_page
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_slider_song(is_home: bool = False):
        try:
            slider_song = []
            if is_home:
                slider_song_items = SliderHome.objects.filter(type=SliderType.song.value,
                                                              SongSlider__is_active=True,
                                                              SongSlider__Song__is_active_link=True)
                if slider_song_items:
                    for slider_song_item in slider_song_items:
                        song_slider = slider_song_item.SongSlider
                        song = song_slider.Song
                        slider_song.append(dict(song_id=song.song_id,
                                                image=song_slider.image_link,
                                                name=song.fa_name,
                                                singer=song.singer.fa_name,
                                                link=song.link, ))
            else:
                song_sliders = SliderSong.objects.select_related("Song__singer").filter(is_show=True, is_active=True,
                                                                                        Song__is_active_link=True, )
                if song_sliders:
                    for song_slider in song_sliders:
                        song = song_slider.Song
                        slider_song.append(dict(song_id=song.song_id,
                                                image=song_slider.image_link,
                                                name=song.fa_name,
                                                singer=song.singer.fa_name,
                                                link=song.link))
            return slider_song
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_song(song: Songs, child: bool = False):
        if not child:
            home_song = {"song_id": int(song.song_id),
                         "fa_name": str(song.fa_name),
                         "en_name": str(song.en_name),
                         "fa_singer": str(song.singer.fa_name) if song.singer else "",
                         "en_singer": str(song.singer.en_name) if song.singer else "",
                         "image_link": str(song.image_link),
                         "length": int(song.length),
                         "link": song.link
                         }
        else:
            home_song = {"song_id": int(song.song_id),
                         "fa_name": str(song.fa_name),
                         "en_name": str(song.en_name),
                         "image_link": str(song.image_link),
                         "length": int(song.length),
                         "link": str(song.link)
                         }
        return home_song

    @staticmethod
    def get_new_songs():
        songs = Songs.objects.select_related("singer").filter(is_podcast=False,
                                                              is_childish=False,
                                                              is_active_image=True,
                                                              is_active_link=True,
                                                              singer__is_active=True
                                                              ).order_by('-song_id')[:10]
        home_songs = map(lambda song: Util_App.get_song(song), songs) if songs else []
        return home_songs

    @staticmethod
    def get_all_popular_songs(page: int = 1):
        home_songs = []
        songs = Songs.objects.select_related("singer").filter(is_podcast=False, is_childish=False,
                                                              is_active_image=True, is_active_link=True,
                                                              singer__is_active=True).order_by('-view_count')
        songs_paginator = Paginator(songs, 10)
        singers_page = songs_paginator.get_page(page)
        data_page = songs_paginator.num_pages
        if singers_page:
            for song in singers_page:
                home_songs.append(Util_App.get_song(song))
        return data_page, home_songs

    @staticmethod
    def get_new_songs_child(count_song: int = 21):
        songs = Songs.objects.filter(is_childish=True, is_active_link=True, is_active_image=True).order_by('-song_id')[
                :count_song]
        home_songs = map(lambda song: Util_App.get_song(song, True), songs) if songs else []
        return home_songs

    @staticmethod
    def get_play_list():
        try:
            playlists = Playlists.objects.filter(songs__is_active_link=True, songs__is_active_image=True,
                                                 is_active=True).distinct()[:10]
            home_play_lists = map(lambda playlist: dict(playlist_id=playlist.playlist_id,
                                                        name=playlist.name,
                                                        cover=playlist.cover), playlists) if playlists else []
            return home_play_lists
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_new_singer():
        singers = Singer_Channel.objects.filter(is_active=True, is_channel=False, songs__is_active_image=True,
                                                songs__is_active_link=True).distinct()[:10]
        home_Singer = map(lambda singer: dict(
            singer_id=singer.singer_id,
            fa_name=singer.fa_name,
            image_link=singer.image_link,
        ), singers) if singers else []
        return home_Singer

    @staticmethod
    def get_all_singer(page: int = 1):
        new_singer = []
        Singers = Singer_Channel.objects.filter(is_channel=False, is_active=True, songs__is_active_image=True,
                                                songs__is_active_link=True).order_by('-singer_id')
        singers_paginator = Paginator(Singers, 10)
        singers_page = singers_paginator.get_page(page)
        data_page = singers_paginator.num_pages
        for Singer in singers_page:
            # songs_singer = Songs.objects.first(singer=Singer, is_active_image=True, is_active_link=True)
            # print("singer:", songs_singer)
            # if not songs_singer.first():
            #     return None, None
            home_Singer = {
                "singer_id": int(Singer.singer_id),
                "fa_name": str(Singer.fa_name),
                "image_link": str(Singer.image_link),
            }
            new_singer.append(home_Singer)
        return data_page, new_singer

    @staticmethod
    def get_popular_songs_singer(Singer_channel: Singer_Channel):
        songs = Singer_channel.song_all_popular[:5]
        home_songs = map(lambda song: Util_App.get_song(song), songs) if songs else []
        return home_songs

    @staticmethod
    def get_five_songs_singer(Singer_channel: Singer_Channel):
        songs = Singer_channel.song_all[:5]
        home_songs = map(lambda song: Util_App.get_song(song), songs) if songs else []
        return home_songs

    @staticmethod
    def get_all_songs_singer(Singer_channel: Singer_Channel, page: int = 1):
        songs = Singer_channel.song_all
        songs_paginator = Paginator(songs, 10)
        songs_page = songs_paginator.get_page(page)
        data_page = songs_paginator.num_pages
        home_songs = map(lambda song: Util_App.get_song(song), songs_page) if songs_page else []
        return data_page, home_songs

    @staticmethod
    def get_all_popular_songs_singer(Singer_channel: Singer_Channel, page: int = 1):
        songs = Singer_channel.song_all_popular
        songs_paginator = Paginator(songs, 10)
        songs_page = songs_paginator.get_page(page)
        data_page = songs_paginator.num_pages
        home_songs = map(lambda song: Util_App.get_song(song), songs_page) if songs_page else []
        return data_page, home_songs

    @staticmethod
    def get_podcast(song: Songs):
        try:
            home_podcast = {"channel_id": int(song.singer.singer_id),
                            "channel_name": str(song.singer.fa_name),
                            "song_id": int(song.song_id),
                            "fa_name": str(song.fa_name),
                            "image_link": str(song.image_link),
                            "link": song.link,
                            }
            return home_podcast
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_new_podcast():
        try:
            songs = Songs.objects.select_related("singer").filter(is_podcast=True,
                                                                  singer__is_channel=True,
                                                                  singer__is_active=True,
                                                                  is_active_image=True,
                                                                  is_active_link=True).order_by(
                '-song_id')[:10]
            home_podcast = map(lambda song: Util_App.get_podcast(song), songs) if songs else []
            return home_podcast
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_all_podcasts(page: int = 1):
        home_podcast = []
        songs = Songs.objects.select_related("singer").filter(is_podcast=True, is_active_link=True,
                                                              is_active_image=True,
                                                              singer__is_active=True).order_by('-view_count')
        songs_paginator = Paginator(songs, 10)
        songs_page = songs_paginator.get_page(page)
        data_page = songs_paginator.num_pages
        if songs_page:
            for song in songs_page:
                home_podcast.append(Util_App.get_podcast(song))
        return data_page, home_podcast

    @staticmethod
    def get_new_channel():
        channels = Singer_Channel.objects.filter(is_channel=True, is_active=True, songs__is_active_image=True,
                                                 songs__is_active_link=True, songs__is_podcast=True).distinct()
        home_channels = map(lambda channel: dict(
            channel_id=channel.singer_id,
            fa_name=channel.fa_name,
            image_link=channel.image_link,
        ), channels) if channels else []
        return home_channels

    @staticmethod
    def get_all_channels(page: int = 1):
        home_channel = []
        channels = Singer_Channel.objects.filter(is_channel=True, is_active=True).order_by('-singer_id')
        channels_paginator = Paginator(channels, 10)
        channels_page = channels_paginator.get_page(page)
        data_page = channels_paginator.num_pages
        if channels_page:
            for channel in channels_page:
                home_channel.append({
                    "channel_id": int(channel.singer_id),
                    "fa_name": str(channel.fa_name),
                    "image_link": str(channel.image_link),
                })
        return data_page, home_channel

    @staticmethod
    def get_songs_playlist(playlist: Playlists, page: int = 1):
        songs = playlist.song_all
        song_paginator = Paginator(songs, 5)
        data_page = song_paginator.num_pages
        song_paginator = song_paginator.get_page(page)
        home_songs = map(lambda song: Util_App.get_song(song), song_paginator) if song_paginator else []
        return data_page, home_songs

    @staticmethod
    def get_popular_songs_playlist(playlist: Playlists, page: int = 1):
        songs = playlist.song_all_popular
        song_paginator = Paginator(songs, 5)
        data_page = song_paginator.num_pages
        song_paginator = song_paginator.get_page(page)
        home_songs = map(lambda song: Util_App.get_song(song), song_paginator) if song_paginator else []
        return data_page, home_songs

    @staticmethod
    def get_home_slider_ads():
        try:
            slider_ads = []
            slider_ads_items = SliderHome.objects.filter(type=SliderType.ads.value, AdsSlider__is_active=True)
            if slider_ads_items:
                slider_ads = [dict(image_url=slider_ads.AdsSlider.image_url,
                                   click_url=slider_ads.AdsSlider.click_url,
                                   title=slider_ads.AdsSlider.title, )
                              for slider_ads in slider_ads_items]
            return slider_ads
        except Exception as e:
            return [str(e)]

    @staticmethod
    def Get_category(cat: VideoCategory):
        return dict(category_id=cat.category_id,
                    image_link=cat.image_link,
                    title=cat.title)

    @staticmethod
    def search(search: str):
        try:
            videos = Videos.objects.filter(Q(fa_name__icontains=search) |
                                           Q(en_name__icontains=search) |
                                           Q(director__icontains=search) |
                                           Q(description__icontains=search) |
                                           Q(country_product__icontains=search) |
                                           Q(videoactors__en_name__icontains=search) |
                                           Q(videoactors__fa_name__icontains=search)) \
                .distinct().order_by("fa_name").filter(Q(is_active_image=True) & Q(is_active_link=True))
            songs = Songs.objects.filter(Q(fa_name__icontains=search) |
                                         Q(en_name__icontains=search) |
                                         Q(description__icontains=search) |
                                         Q(singer__fa_name__icontains=search)) \
                .distinct().order_by("fa_name").filter(Q(is_active_link=True) & Q(is_active_image=True))
            return {
                'video': [Util_App.get_video(video) for video in videos],
                'song': [Util_App.get_song(song) for song in songs]
            }
        except Exception as e:
            return [str(e)]

import random

from django.core.paginator import Paginator
from django.db.models import Q, Prefetch

from apiApp.models import *
from apiWeb.models import *
from chamedoon.util import util
from apiApp.models import VideoActors

from apiApp.models import OrderByPlaylist

class Util_Web:
    @staticmethod
    def get_slider_ads():
        try:
            slider_ads = []
            slider_ads_items = SliderHome.objects.select_related("AdsSlider").filter(type=SliderType.ads.value,
                                                                                     AdsSlider__is_active=True)
            if slider_ads_items:
                slider_ads = map(lambda slider_ad: dict(image_url=slider_ad.AdsSlider.image_url,
                                                        click_url=slider_ad.AdsSlider.click_url,
                                                        title=slider_ad.AdsSlider.title), slider_ads_items)
            return slider_ads
        except Exception as e:
            return []

    @staticmethod
    def get_video(video: Videos):
        try:
            home_video = {"video_id": int(video.video_id),
                          "fa_name": str(video.fa_name),
                          "en_name": str(video.en_name),
                          "slug": str(video.slug),
                          "description": str(video.description),
                          "imdb_rating": int(video.imdb_rating),
                          "image_link": str(video.image_link),
                          "link": str(video.link)}
            return home_video
        except Exception as e:
            print("Error get_video :", str(e))
            return str(e)

    @staticmethod
    def get_new_videos():
        try:
            videos = Videos.objects.filter(is_childish=False, is_active_image=True, is_active_link=True).order_by(
                '-video_id')[:10]
            home_videos = map(lambda video: Util_Web.get_video(video), videos) if videos else []
            return home_videos
        except Exception as e:
            print("Error get_video :", str(e))
            return str(e)

    @staticmethod
    def get_most_visited_videos():
        videos = Videos.objects.filter(is_childish=False, is_active_image=True, is_active_link=True,
                                       videoactors__is_active=True).distinct().order_by('-view_count')[:10]
        home_videos = map(lambda video: Util_Web.get_video(video), videos) if videos else []
        return home_videos

    @staticmethod
    def get_videos_category(cat_id: int, page: int = 1):
        try:
            home_videos = []
            data_page = 0
            videos = Videos.objects.filter(category_id=cat_id, is_childish=False, is_active_image=True,
                                           is_active_link=True).order_by("-view_count")
            if videos:
                videos_Paginator = Paginator(videos, 10)
                videos_page = videos_Paginator.get_page(page)
                data_page = videos_Paginator.num_pages
                home_videos = [Util_Web.get_video(video) for video in videos_page]
            return home_videos, data_page
        except Exception as e:
            return [str(e)]

    @staticmethod
    def Get_category(cat: VideoCategory):
        return dict(category_id=cat.category_id,
                    image_link=cat.image_link,
                    title=cat.title)

    @staticmethod
    def get_slider_video(is_home: bool = False):
        try:
            slider_video = []
            if is_home:
                prefetch = Prefetch("VideoSlider__video__videoactors_set",
                                    queryset=VideoActors.objects.filter(is_active=True).only("actor_id", "fa_name"),
                                    to_attr="actor_all"
                                    )
                slider_video_items = SliderHome.objects.select_related("VideoSlider__video").prefetch_related(
                    prefetch).filter(
                    type=SliderType.video.value,
                    VideoSlider__is_active=True,
                    VideoSlider__video__is_active_link=True,
                    VideoSlider__video__is_active_image=True,
                )
                for slider_video_item in slider_video_items:
                    video_slider = slider_video_item.VideoSlider
                    if video_slider:
                        video = video_slider.video
                        actors = map(lambda x: {"actor_id": x.actor_id, "fa_name": x.fa_name},
                                     video_slider.video.actor_all)
                        slider_video.append(dict(video_id=int(video.video_id),
                                                 image_link=str(video_slider.image_link),
                                                 fa_name=str(video.fa_name),
                                                 en_name=str(video.en_name),
                                                 slug=str(video.slug),
                                                 director=str(video.director),
                                                 summary=str(video.summary),
                                                 actors=actors,
                                                 Preview=str(video.preview_link) if video.is_active_preview else None,
                                                 link=str(video.link)))
            else:

                prefetch = Prefetch("video__videoactors_set",
                                    queryset=VideoActors.objects.filter(is_active=True).only("actor_id", "fa_name"),
                                    to_attr="actor_all"
                                    )
                video_sliders = SliderVideo.objects.select_related("video").prefetch_related(prefetch).filter(
                    is_show=True,
                    is_childish=False,
                    is_active=True,
                    video__is_active_link=True,
                    video__is_active_image=True, )
                if video_sliders:
                    for video_slider in video_sliders:
                        video = video_slider.video
                        actors = map(lambda actor: {"actor_id": actor.actor_id, "fa_name": actor.fa_name},
                                     video_slider.video.actor_all)

                        print("aa:", actors)
                        slider_video.append(dict(video_id=int(video.video_id),
                                                 image_link=str(video_slider.image_link),
                                                 fa_name=str(video.fa_name),
                                                 en_name=str(video.en_name),
                                                 slug=str(video.slug),
                                                 director=str(video.director),
                                                 summary=str(video.summary),
                                                 actors=actors,
                                                 Preview=str(video.preview_link) if video.is_active_preview else None,
                                                 link=str(video.link)))
            return slider_video
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_slider_song(is_home: bool = False):
        try:
            slider_song = []
            if is_home:
                slider_song_items = SliderHome.objects.select_related("SongSlider__Song__singer"). \
                    filter(type=SliderType.song.value,
                           SongSlider__is_active=True,
                           SongSlider__Song__is_active_link=True)
                if slider_song_items:
                    for slider_song_item in slider_song_items:
                        song_slider = slider_song_item.SongSlider
                        song = song_slider.Song
                        style_songs = song.songstyles_set.all().values("style_id", "name")
                        slider_song.append(dict(song_id=song.song_id,
                                                image_link=str(song_slider.image_link),
                                                fa_name=str(song.fa_name),
                                                en_name=str(song.en_name),
                                                singer=str(song.singer.fa_name),
                                                style_songs=style_songs,
                                                tarane=str(song_slider.tarane),
                                                tuning=str(song_slider.tuning),
                                                lyric=str(song_slider.lyric),
                                                link=song.link))
            else:
                song_sliders = SliderSong.objects.prefetch_related("Song__songstyles_set"). \
                    filter(is_show=True, is_active=True, Song__is_active_link=True, )
                if song_sliders:
                    for song_slider in song_sliders:
                        song = song_slider.Song
                        style = song.songstyles_set.all().values("style_id", "name")
                        slider_song.append(dict(song_id=song.song_id,
                                                image_link=str(song_slider.image_link),
                                                fa_name=str(song.fa_name),
                                                en_name=str(song.en_name),
                                                singer=str(song.singer.fa_name),
                                                style_songs=style,
                                                tarane=str(song_slider.tarane),
                                                tuning=str(song_slider.tuning),
                                                lyric=str(song_slider.lyric),
                                                link=song.link))
                    # print("b  :", str(slider_song))
            return slider_song
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_song(song: Songs):
        try:
            home_song = {"song_id": int(song.song_id),
                         "fa_name": str(song.fa_name),
                         "en_name": str(song.en_name),
                         "image_link": str(song.image_link),
                         "link": song.link,
                         "singer": str(song.singer.fa_name) if song.singer else ""}
            return home_song
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_song_slider():
        try:
            song_slider_result = []
            song_sliders = SliderSong.objects.select_related("Song__singer").filter(is_show=True, is_active=True,
                                                                                    Song__is_active_link=True)
            if song_sliders:
                for song_slider in song_sliders:
                    song = song_slider.Song
                    song_slider_result.append(dict(song_id=song.song_id,
                                                   image_link=str(song_slider.image_link),
                                                   fa_name=str(song.fa_name),
                                                   en_name=str(song.en_name),
                                                   singer=str(song.singer.fa_name),
                                                   tarane=str(song_slider.tarane),
                                                   tuning=str(song_slider.tuning),
                                                   style_songs=song.songstyles_set.values_list("name", flat=True),
                                                   lyric=str(song_slider.lyric),
                                                   release_date=str(song_slider.release_date),
                                                   link=song.link))
            return song_slider_result
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_song_playlists():
        try:
            playlists_result = Playlists.objects.filter(is_active=True).values().order_by('-playlist_id')[:10]
            return playlists_result
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_all_playlists():
        try:
            playlists_all = Playlists.objects.filter(is_active=True).values().order_by('-playlist_id')
            return playlists_all
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_playlist_songs(playlist_id: int):
        try:
            result_songs = []
            prefetch = Prefetch('songs',
                                queryset=Songs.objects.select_related("singer").filter(is_active_image=True,
                                                                                       is_active_link=True),
                                to_attr="all_songs")
            playlist = Playlists.objects.prefetch_related(prefetch).filter(playlist_id=playlist_id,
                                                                           is_active=True).first()
            if playlist:
                songs = playlist.all_songs
                result_songs = list(map(lambda song: dict(
                    song_id=str(song.song_id),
                    fa_name=str(song.fa_name),
                    en_name=str(song.en_name),
                    image_link=str(song.image_link),
                    singer=str(song.singer.fa_name),
                    link=str(song.link),
                    view_count=int(song.view_count)
                ), songs))
                if playlist.sort_by == OrderByPlaylist.random.value:
                    random.shuffle(result_songs)
                if playlist.sort_by == OrderByPlaylist.latest.value:
                    result_songs = sorted(result_songs, key=lambda k: k['song_id'], reverse=True)
                if playlist.sort_by == OrderByPlaylist.most_visited.value:
                    result_songs = sorted(result_songs, key=lambda k: k['view_count'], reverse=True)
                if playlist.sort_by == OrderByPlaylist.en_name.value:
                    result_songs = sorted(result_songs, key=lambda k: k['en_name'], )
                for song in result_songs:
                    song.pop("view_count")
            return result_songs[:10]
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_song_singers():
        try:
            singers_result = Singer_Channel.objects.filter(is_channel=False, is_active=True). \
                                 values('singer_id',
                                        'fa_name',
                                        'en_name',
                                        'image_link')[:10]
            return singers_result
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_all_singers():
        try:
            singers_all = Singer_Channel.objects.filter(is_channel=False, is_active=True).values('singer_id', 'fa_name',
                                                                                                 'en_name',
                                                                                                 'image_link')
            return singers_all
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_singer_songs(singer_id: int):
        try:
            result_songs = []
            prefetch = Prefetch('songs_set',
                                queryset=Songs.objects.select_related("singer").filter(is_active_image=True,
                                                                                       is_active_link=True),
                                to_attr="songs_ten")
            singer = Singer_Channel.objects.prefetch_related(prefetch).filter(singer_id=singer_id,
                                                                              is_active=True).first()
            if singer:
                songs = singer.songs_ten[:10]
                result_songs = map(lambda song: dict(
                    song_id=str(song.song_id),
                    fa_name=str(song.fa_name),
                    en_name=str(song.en_name),
                    image_link=str(song.image_link),
                    singer=str(song.singer.fa_name),
                    link=str(song.link),
                ), songs)
            return result_songs
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_latest_songs():
        try:
            latest_songs = Songs.objects.select_related("singer").filter(is_podcast=False, is_childish=False,
                                                                         is_active_image=True,
                                                                         is_active_link=True).order_by('-song_id')[:10]
            result_songs = map(lambda song: dict(
                song_id=str(song.song_id),
                fa_name=str(song.fa_name),
                en_name=str(song.en_name),
                image_link=str(song.image_link),
                singer=str(song.singer.fa_name),
                link=str(song.link),
            ), latest_songs) if latest_songs else []
            return result_songs

        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_popular_songs():
        try:
            latest_songs = Songs.objects.select_related("singer").filter(is_podcast=False, is_childish=False,
                                                                         is_active_image=True,
                                                                         is_active_link=True). \
                               order_by('-view_count')[:10]
            result_songs = map(lambda song: dict(
                song_id=str(song.song_id),
                fa_name=str(song.fa_name),
                en_name=str(song.en_name),
                image_link=str(song.image_link),
                singer=str(song.singer.fa_name),
                link=str(song.link),
            ), latest_songs) if latest_songs else []
            return result_songs

        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_latest_podcasts():
        try:
            latest_podcasts = Songs.objects.select_related("singer").filter(is_podcast=True, is_childish=False,
                                                                            is_active_image=True,
                                                                            is_active_link=True).order_by('-song_id')[
                              :10]
            result_podcasts = map(lambda podcast: dict(
                song_id=str(podcast.song_id),
                fa_name=str(podcast.fa_name),
                en_name=str(podcast.en_name),
                image_link=str(podcast.image_link),
                singer=str(podcast.singer.fa_name),
                link=str(podcast.link),
            ), latest_podcasts) if latest_podcasts else []
            return result_podcasts
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_popular_podcasts():
        try:
            popular_podcasts = Songs.objects.select_related("singer").filter(is_podcast=True, is_childish=False,
                                                                             is_active_image=True,
                                                                             is_active_link=True).order_by(
                '-view_count')[:10]
            result_podcasts = map(lambda podcast: dict(
                song_id=str(podcast.song_id),
                fa_name=str(podcast.fa_name),
                en_name=str(podcast.en_name),
                image_link=str(podcast.image_link),
                singer=str(podcast.singer.fa_name),
                link=str(podcast.link),
            ), popular_podcasts) if popular_podcasts else []
            return result_podcasts
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_channels():
        try:
            channels_result = Singer_Channel.objects.filter(is_channel=True, is_active=True). \
                                  values('singer_id', 'fa_name', 'en_name', 'image_link')[:10]
            return channels_result
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_channel_all():
        try:
            channels_result = Singer_Channel.objects.filter(is_channel=True, is_active=True).values('singer_id',
                                                                                                    'fa_name',
                                                                                                    'en_name',
                                                                                                    'image_link')
            return channels_result
        except Exception as e:
            return [str(e)]

    @staticmethod
    def get_channel_songs(channel_id: int):
        try:
            result_songs = []
            prefetch = Prefetch('songs_set',
                                queryset=Songs.objects.select_related("singer").filter(is_active_image=True,
                                                                                       is_active_link=True),
                                to_attr="songs_ten")
            channel = Singer_Channel.objects.prefetch_related(prefetch).filter(is_channel=True,
                                                                               singer_id=channel_id,
                                                                               is_active=True).first()
            if channel:
                songs = channel.songs_ten[:10]
                result_songs = map(lambda song: dict(
                    song_id=str(song.song_id),
                    fa_name=str(song.fa_name),
                    en_name=str(song.en_name),
                    image_link=str(song.image_link),
                    channel=str(song.singer.fa_name),
                    link=str(song.link),
                ), songs)
            return result_songs
        except Exception as e:
            return [str(e)]

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
            songs = Songs.objects.select_related('singer').filter(Q(fa_name__icontains=search) |
                                                                  Q(en_name__icontains=search) |
                                                                  Q(description__icontains=search) |
                                                                  Q(singer__fa_name__icontains=search)) \
                .distinct().order_by("fa_name").filter(Q(is_active_link=True) & Q(is_active_image=True))
            return {
                'video': map(lambda video: Util_Web.get_video(video), videos),
                'song': map(lambda song: Util_Web.get_song(song), songs),
            }
        except Exception as e:
            return [str(e)]

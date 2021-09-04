import json

from django.test import Client
from apiApp.models import *
from apiApp.models import Videos, Songs, Ads, VideoCategory
from apiWeb.models.Slider import *
from apiWeb.util import Util_Web
from chamedoon.util import util

client = Client()

from django.test import TestCase


def create_category(category_id: int = 1, is_active=True):
    VideoCategory(
        category_id=category_id,
        is_active=is_active,
        image_link="test",
        title="tets").save()


def create_video(video_id, is_active_link=True, is_active_image=True, is_childish=False, category_id: int = 1):
    video = Videos(
        video_id=video_id,
        fa_name="test",
        en_name="test",
        image_link="test",
        description="test",
        length=0,
        summary="test",
        director="test",
        category_id=category_id,
        link="test",
        is_active_image=is_active_link,
        is_active_link=is_active_image,
        is_childish=is_childish,
    )
    video.save()
    return video


def create_singer(singer_id, is_active=True, is_channel=False):
    singer = Singer_Channel(
        singer_id=singer_id,
        fa_name="test",
        en_name="test",
        image_link="test",
        is_active=is_active,
        is_channel=is_channel
    )
    singer.save()
    return singer


def create_song(song_id, is_active_image=True, is_active_link=True, is_childish=False, singer_id: int = 1,
                is_podcast=False):
    Songs(
        song_id=song_id,
        fa_name="test",
        en_name="test",
        image_link="test",
        length=0,
        is_active_image=is_active_image,
        is_active_link=is_active_link,
        is_childish=is_childish,
        is_podcast=is_podcast,
        description="",
        link="test",
        singer_id=singer_id,
    ).save()


##############################
'''integration tests'''


class HomeCases(TestCase):
    def test_get_home_videos(self):
        VideoCategory(
            category_id=1,
            is_active=True,
            image_link="test",
            title="tets").save()
        VideoCategory(
            category_id=2,
            is_active=True,
            image_link="test",
            title="tets").save()

        for i in range(13):
            video = Videos(
                video_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                description="",
                length=0,
                summary="",
                director="test",
                category_id=1 if i % 2 == 0 else 2,
                is_active_image=True,
                is_active_link=True
            )
            video.save()
        get_video_ok_test = self.client.get('/api/web/home/videos', data={})
        assert (get_video_ok_test.status_code == 200), str(get_video_ok_test.content)
        res = json.loads(str(get_video_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Videos.objects.filter(en_name="test").delete()
        VideoCategory.objects.filter(title="test").delete()

        get_video_ok_test = self.client.get('/api/web/home/videos', data={})
        assert (get_video_ok_test.status_code == 200), str(get_video_ok_test.content)
        res = json.loads(str(get_video_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_home_songs(self):
        singer = Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        )
        singer.save()
        for i in range(13):
            song = Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                description="",
                link="test",
                singer=singer
            )
            song.save()
        get_song_ok_test = self.client.get('/api/web/home/songs', data={})
        assert (get_song_ok_test.status_code == 200), str(get_song_ok_test.content)
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Singer_Channel.objects.filter(en_name="test").delete()
        Songs.objects.filter(en_name="test").delete()

        get_song_ok_test = self.client.get('/api/web/home/songs', data={})
        assert (get_song_ok_test.status_code == 200), str(get_song_ok_test.content)
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_home_podcasts(self):
        singer = Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        )
        singer.save()
        for i in range(10):
            podcast = Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                description="",
                link="test",
                singer=singer,
                is_podcast=True
            )
            podcast.save()
        get_podcast_ok_test = self.client.get('/api/web/home/podcasts', data={})
        assert (get_podcast_ok_test.status_code == 200), str(get_podcast_ok_test.content)
        res = json.loads(str(get_podcast_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Singer_Channel.objects.filter(en_name="test").delete()
        Songs.objects.filter(en_name="test").delete()

        get_podcast_ok_test = self.client.get('/api/web/home/podcasts', data={})
        assert (get_podcast_ok_test.status_code == 200), str(get_podcast_ok_test.content)
        res = json.loads(str(get_podcast_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_home_ads(self):
        for i in range(10):
            ad = Ads(
                ad_id=i,
                image_url="test",
                is_active=True,
                is_video_ads=False
            )
            ad.save()
        get_ads_ok_test = self.client.get('/api/web/home/ads', data={})
        assert (get_ads_ok_test.status_code == 200), str(get_ads_ok_test.content)
        res = json.loads(str(get_ads_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 3), str(res['data'])

        Ads.objects.filter(image_url="test").delete()

        get_ads_ok_test = self.client.get('/api/web/home/ads', data={})
        assert (get_ads_ok_test.status_code == 200), str(get_ads_ok_test.content)
        res = json.loads(str(get_ads_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_home_slider(self):
        VideoCategory(
            category_id=1,
            is_active=True,
            image_link="test",
            title="test").save()
        video = Videos(
            video_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            description="",
            length=0,
            summary="",
            director="test",
            category_id=1,
            is_active_image=True,
            is_active_link=True
        )
        video.save()
        Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        ).save()
        Songs(
            song_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            length=0,
            is_active_image=True,
            is_active_link=True,
            description="",
            link="test",
            singer_id=1
        ).save()
        Ads(
            ad_id=1,
            image_url="test",
            is_active=True,
            is_video_ads=False
        ).save()
        for i in range(10):
            actor = VideoActors(
                actor_id=i,
                fa_name='test',
                en_name='test',
                avatar='test',
                is_active=True
            )
            actor.save()
            actor.videos.add(video)
        for i in range(10):
            video_slider = SliderVideo(
                slider_id=i,
                is_active=True,
                image_link="test",
                video_id=1,
                is_show=True
            )
            video_slider.save()
            video_home_slider = SliderHome(
                slider_id=i,
                VideoSlider=video_slider,
                name='test',
                type=0
            )
            video_home_slider.save()
        for i in range(10):
            song_slider = SliderSong(
                slider_id=i,
                image_link="test",
                is_active=True,
                is_show=True,
                tarane="test",
                tuning="test",
                Song_id=1,
                release_date="test",
                lyric="test",
            )
            song_slider.save()
            song_home_slider = SliderHome(
                slider_id=i + 10,
                SongSlider=song_slider,
                name='test',
                type=1
            )
            song_home_slider.save()
        for i in range(10):
            ad_slider = SliderAds(
                slider_id=i,
                is_active=True,
                title="test",
            )
            ad_slider.save()
            ad_home_slider = SliderHome(
                slider_id=i + 20,
                AdsSlider=ad_slider,
                name='test',
                type=2
            )
            ad_home_slider.save()

        get_slider_ok_test = self.client.get('/api/web/home/main-slider', data={})
        assert (get_slider_ok_test.status_code == 200), str(get_slider_ok_test.content)
        res = json.loads(str(get_slider_ok_test.content.decode("utf8")))
        assert (res['data']['slider_video'].__len__() == 10), str(res['data']['slider_video'])
        assert (res['data']['slider_song'].__len__() == 10), str(res['data']['slider_song'])
        assert (res['data']['slider_ads'].__len__() == 10), str(res['data']['slider_ads'])

        VideoCategory.objects.filter(title='test').delete()
        Videos.objects.filter(en_name='test').delete()
        VideoActors.objects.filter(en_name='test').delete()
        Singer_Channel.objects.filter(en_name='test').delete()
        Songs.objects.filter(en_name='test').delete()
        SliderAds.objects.filter(title="test").delete()
        SliderHome.objects.filter(name='test').delete()

        get_slider_ok_test = self.client.get('/api/web/home/main-slider', data={})
        assert (get_slider_ok_test.status_code == 200), str(get_slider_ok_test.content)
        res = json.loads(str(get_slider_ok_test.content.decode("utf8")))
        assert (res['data']['slider_video'].__len__() == 0), str(res['data']['slider_video'])
        assert (res['data']['slider_song'].__len__() == 0), str(res['data']['slider_song'])
        assert (res['data']['slider_ads'].__len__() == 0), str(res['data']['slider_ads'])

    def test_get_home_search(self):
        VideoCategory(
            category_id=1,
            is_active=True,
            image_link="test",
            title="test").save()
        Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        ).save()

        for i in range(10):
            video = Videos(
                video_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                description="",
                length=0,
                summary="",
                director="test",
                category_id=1,
                is_active_image=True,
                is_active_link=True
            )
            video.save()
        for i in range(10):
            Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                description="",
                link="test",
                singer_id=1
            ).save()
        get_search_ok_test = self.client.get('/api/web/search', data={'q': 'test'})
        assert (get_search_ok_test.status_code == 200), str(get_search_ok_test.content)
        res = json.loads(str(get_search_ok_test.content.decode("utf8")))
        assert (res['data']['video'].__len__() == 10), str(res['data']['video'])
        assert (res['data']['song'].__len__() == 10), str(res['data']['song'])

        VideoCategory.objects.filter(title="test").delete()
        Videos.objects.filter(en_name="test").delete()
        Singer_Channel.objects.filter(en_name="test").delete()
        Songs.objects.filter(en_name="test").delete()

        get_search_ok_test = self.client.get('/api/web/search', data={'q': 'test'})
        assert (get_search_ok_test.status_code == 200), str(get_search_ok_test.content)
        res = json.loads(str(get_search_ok_test.content.decode("utf8")))
        assert (res['data']['video'].__len__() == 0), str(res['data']['video'])
        assert (res['data']['song'].__len__() == 0), str(res['data']['song'])


class MovieCases(TestCase):
    def test_get_movie_slider(self):
        VideoCategory(
            category_id=1,
            is_active=True,
            image_link="test",
            title="test").save()
        video = Videos(
            video_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            description="",
            length=0,
            summary="",
            director="test",
            category_id=1,
            is_active_image=True,
            is_active_link=True)
        video.save()

        for i in range(10):
            SliderVideo(
                slider_id=i,
                is_active=True,
                image_link="test",
                video_id=1,
                is_show=True).save()

        get_slider_ok_test = self.client.get('/api/web/movies/slider', data={})
        assert (get_slider_ok_test.status_code == 200), str(get_slider_ok_test.content)
        res = json.loads(str(get_slider_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Videos.objects.filter(en_name="test").delete()
        VideoCategory.objects.filter(title="test").delete()

        get_slider_ok_test = self.client.get('/api/web/movies/slider', data={})
        assert (get_slider_ok_test.status_code == 200), str(get_slider_ok_test.content)
        res = json.loads(str(get_slider_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_movie_cat(self):
        for i in range(10):
            VideoCategory(
                category_id=i,
                is_active=True,
                title="test"
            ).save()
            Videos(
                video_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                description="",
                length=0,
                summary="",
                director="test",
                category_id=i,
                is_active_image=True,
                is_active_link=True).save()

        get_cat_ok_test = self.client.get('/api/web/movies/cat', data={})
        assert (get_cat_ok_test.status_code == 200), str(get_cat_ok_test.content)
        res = json.loads(str(get_cat_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Videos.objects.filter(en_name='test').delete()

        get_cat_ok_test = self.client.get('/api/web/movies/cat', data={})
        assert (get_cat_ok_test.status_code == 200), str(get_cat_ok_test.content)
        res = json.loads(str(get_cat_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_movie_single_cat(self):
        VideoCategory(
            category_id=0,
            is_active=True,
            title="test"
        ).save()
        VideoCategory(
            category_id=1,
            is_active=True,
            title="test"
        ).save()
        for i in range(10):
            Videos(
                video_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                description="",
                length=0,
                summary="",
                director="test",
                category_id=0,
                is_active_image=True,
                is_active_link=True
            ).save()
        for i in range(10):
            Videos(
                video_id=i + 10,
                fa_name="test",
                en_name="test",
                image_link="test",
                description="",
                length=1,
                summary="",
                director="test",
                category_id=1,
                is_active_image=True,
                is_active_link=True

            ).save()

        get_cat_ok_test = self.client.get('/api/web/movies/cat/0', data={})
        assert (get_cat_ok_test.status_code == 200), str(get_cat_ok_test.content)
        res = json.loads(str(get_cat_ok_test.content.decode("utf8")))
        assert (res['data']['videos'].__len__() == 10), str(res['data']['videos'])

        get_cat_ok_test_2 = self.client.get('/api/web/movies/cat/1', data={})
        assert (get_cat_ok_test_2.status_code == 200), str(get_cat_ok_test_2.content)
        res = json.loads(str(get_cat_ok_test_2.content.decode("utf8")))
        assert (res['data']['videos'].__len__() == 10), str(res['data']['videos'])

        Videos.objects.filter(en_name="test").delete()

        get_cat_ok_test = self.client.get('/api/web/movies/cat/0', data={})
        assert (get_cat_ok_test.status_code == 200), str(get_cat_ok_test.content)
        res = json.loads(str(get_cat_ok_test.content.decode("utf8")))
        assert (res['data']['videos'].__len__() == 0), str(res['data']['videos'])

        get_cat_ok_test_2 = self.client.get('/api/web/movies/cat/1', data={})
        assert (get_cat_ok_test_2.status_code == 200), str(get_cat_ok_test_2.content)
        res = json.loads(str(get_cat_ok_test_2.content.decode("utf8")))
        assert (res['data']['videos'].__len__() == 0), str(res['data']['videos'])

        VideoCategory.objects.filter(title="test").delete()

        get_cat_fail_test = self.client.get('/api/web/movies/cat/0', data={})
        assert (get_cat_fail_test.status_code == 404), str(get_cat_fail_test.content)

        get_cat_fail_test_2 = self.client.get('/api/web/movies/cat/1', data={})
        assert (get_cat_fail_test_2.status_code == 404), str(get_cat_fail_test_2.content)

    def test_get_movie_new(self):
        for i in range(13):
            Videos(
                video_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                description="",
                length=1,
                summary="",
                director="test",
                category_id=1,
                is_active_image=True,
                is_active_link=True).save()

        get_cat_ok_test = self.client.get('/api/web/movies/newVideo', data={})
        assert (get_cat_ok_test.status_code == 200), str(get_cat_ok_test.content)
        res = json.loads(str(get_cat_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Videos.objects.filter(en_name="test").delete()

        get_cat_ok_test = self.client.get('/api/web/movies/newVideo', data={})
        assert (get_cat_ok_test.status_code == 200), str(get_cat_ok_test.content)
        res = json.loads(str(get_cat_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_movie_ads(self):
        for i in range(10):
            Ads(
                ad_id=i,
                is_video_ads=False,
                is_active=True,
                click_url="test").save()

        get_cat_ok_test = self.client.get('/api/web/movies/ads', data={})
        assert (get_cat_ok_test.status_code == 200), str(get_cat_ok_test.content)
        res = json.loads(str(get_cat_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 3), str(res['data'])

        Ads.objects.filter(click_url="test").delete()

        get_cat_ok_test = self.client.get('/api/web/movies/ads', data={})
        assert (get_cat_ok_test.status_code == 200), str(get_cat_ok_test.content)
        res = json.loads(str(get_cat_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_movie_video_ads(self):
        VideoCategory(
            category_id=1,
            is_active=True,
            image_link="test",
            title="test").save()
        Videos(
            video_id=0,
            fa_name="test",
            en_name="test",
            image_link="test",
            description="",
            length=1,
            summary="",
            director="test",
            is_active_image=True,
            category_id=1,
            is_active_link=True).save()
        for i in range(10):
            Ads(
                ad_id=i,
                is_video_ads=True,
                video_id=0,
                is_active=True,
                click_url="test").save()

        get_cat_ok_test = self.client.get('/api/web/movies/videoAds', data={})
        assert (get_cat_ok_test.status_code == 200), str(get_cat_ok_test.content)
        res = json.loads(str(get_cat_ok_test.content.decode("utf8")))
        assert (bool(res['data'])), str(res['data'])

        Ads.objects.filter(click_url="test").delete()

        get_cat_ok_test = self.client.get('/api/web/movies/videoAds', data={})
        assert (get_cat_ok_test.status_code == 200), str(get_cat_ok_test.content)
        res = json.loads(str(get_cat_ok_test.content.decode("utf8")))
        assert (not bool(res['data'])), str(res['data'])

    # def test_get_one_video(self):
    #     VideoCategory(
    #         category_id=1,
    #         is_active=True,
    #         image_link="test",
    #         title="test").save()
    #     genre = VideoGenres(
    #         genre_id=0,
    #         name="test")
    #     genre.save()
    #     video_test = Videos(
    #         video_id=0,
    #         fa_name="test",
    #         en_name="test",
    #         image_link="test",
    #         description="",
    #         length=1,
    #         summary="",
    #         director="test",
    #         category_id=1,
    #         slug="test-test",
    #         is_active_image=True,
    #         is_active_link=True)
    #     video_test.save()
    #     genre.videos.add(video_test)
    #
    #     for i in range(10):
    #         actor = VideoActors(
    #             actor_id=i,
    #             fa_name='test',
    #             en_name='test',
    #             avatar='test',
    #             is_active=True)
    #         actor.save()
    #         actor.videos.add(video_test)
    #
    #     for i in range(1, 14):
    #         video = Videos(
    #             video_id=i,
    #             fa_name="test",
    #             en_name="test",
    #             image_link="test",
    #             description="",
    #             length=1,
    #             summary="",
    #             director="test",
    #             category_id=1,
    #             is_active_image=True,
    #             is_active_link=True)
    #         video.save()
    #         genre.videos.add(video)
    #
    #     for i in range(10):
    #         Ads(
    #             ad_id=i,
    #             is_video_ads=False,
    #             is_active=True,
    #             click_url="test").save()
    #
    #     for i in range(10):
    #         VideoImages(
    #             image_id=i,
    #             video_id=0,
    #             is_active=True,
    #             name='test').save()
    #
    #     get_one_video_ok_test = self.client.get('/api/web/movies/test-test', data={})
    #     assert (get_one_video_ok_test.status_code == 200), str(get_one_video_ok_test.content)
    #     res = json.loads(str(get_one_video_ok_test.content.decode("utf8")))
    #     assert (res['data'][0]['genres'].__len__() == 1), str(res['data']['genres'])
    #     assert (res['data'][0]['actors'].__len__() == 10), str(res['data']['actors'])
    #     assert (res['data'][0]['similar_videos'].__len__() == 10), str(res['data']['similar_videos'])
    #     assert (res['data'][0]['ads'].__len__() == 3), str(res['data']['ads'])
    #     assert (res['data'][0]['images'].__len__() == 10), str(res['data']['images'])
    #
    #     Videos.objects.filter(en_name='test').delete()
    #     VideoCategory.objects.filter(title='test').delete()
    #     VideoImages.objects.filter(name='test').delete()
    #     Ads.objects.filter(click_url='test').delete()
    #
    #     get_one_video_fail_test = self.client.get('/api/web/movies/test-test', data={})
    #     assert (get_one_video_fail_test.status_code == 404), str(get_one_video_fail_test.content)


class SongCases(TestCase):
    def test_get_song_slider(self):
        Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        ).save()
        song_1 = Songs(
            song_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            length=0,
            is_active_image=True,
            is_active_link=True,
            description="",
            link="test",
            singer_id=1
        )
        song_1.save()
        song_2 = Songs(
            song_id=2,
            fa_name="test",
            en_name="test",
            image_link="test",
            length=0,
            is_active_image=True,
            is_active_link=True,
            description="",
            link="test",
            singer_id=1
        )
        song_2.save()
        style = SongStyles(
            name="test",
            style_id=1,
        )
        style.save()
        style.songs.add(song_1, song_2)
        for i in range(13):
            song_slider = SliderSong(
                slider_id=i,
                image_link="test",
                is_active=True,
                is_show=True,
                tarane="test",
                tuning="test",
                Song_id=1 if i % 2 else 2,
                release_date="test",
                lyric="test",
            )
            song_slider.save()
        get_slider_ok_test = self.client.get('/api/web/songs/slider', data={})
        assert (get_slider_ok_test.status_code == 200), str(get_slider_ok_test.content)
        res = json.loads(str(get_slider_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 13), str(res['data'])

        SliderSong.objects.filter(tarane="test").delete()
        Songs.objects.filter(en_name="test").delete()

        get_slider_ok_test = self.client.get('/api/web/songs/slider', data={})
        assert (get_slider_ok_test.status_code == 200), str(get_slider_ok_test.content)
        res = json.loads(str(get_slider_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_song_popular(self):
        singer = Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        )
        singer.save()
        for i in range(13):
            song = Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                description="",
                link="test",
                view_count=i,
                singer=singer
            )
            song.save()
        get_song_ok_test = self.client.get('/api/web/songs/latest', data={})
        assert (get_song_ok_test.status_code == 200), str(get_song_ok_test.content)
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Singer_Channel.objects.filter(en_name="test").delete()
        Songs.objects.filter(en_name="test").delete()

        get_song_ok_test = self.client.get('/api/web/songs/latest', data={})
        assert (get_song_ok_test.status_code == 200), str(get_song_ok_test.content)
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_song_latest(self):
        singer = Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        )
        singer.save()
        for i in range(13):
            song = Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                description="",
                link="test",
                singer=singer
            )
            song.save()
        get_song_ok_test = self.client.get('/api/web/songs/latest', data={})
        assert (get_song_ok_test.status_code == 200), str(get_song_ok_test.content)
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Singer_Channel.objects.filter(en_name="test").delete()
        Songs.objects.filter(en_name="test").delete()

        get_song_ok_test = self.client.get('/api/web/songs/latest', data={})
        assert (get_song_ok_test.status_code == 200), str(get_song_ok_test.content)
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_song_popular(self):
        singer = Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        )
        singer.save()
        for i in range(13):
            song = Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                description="",
                link="test",
                view_count=i,
                singer_id=1
            )
            song.save()
        get_song_ok_test = self.client.get('/api/web/songs/latest', data={})
        assert (get_song_ok_test.status_code == 200), str(get_song_ok_test.content)
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Singer_Channel.objects.filter(en_name="test").delete()
        Songs.objects.filter(en_name="test").delete()

        get_song_ok_test = self.client.get('/api/web/songs/latest', data={})
        assert (get_song_ok_test.status_code == 200), str(get_song_ok_test.content)
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_podcast_latest(self):
        singer = Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
            is_channel=True
        )
        singer.save()
        for i in range(13):
            song = Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                is_podcast=True,
                description="",
                link="test",
                singer=singer
            )
            song.save()
        get_podcast_ok_test = self.client.get('/api/web/songs/podcasts/latest', data={})
        assert (get_podcast_ok_test.status_code == 200), str(get_podcast_ok_test.content)
        res = json.loads(str(get_podcast_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Singer_Channel.objects.filter(en_name="test").delete()
        Songs.objects.filter(en_name="test").delete()

        get_podcast_ok_test = self.client.get('/api/web/songs/podcasts/latest', data={})
        assert (get_podcast_ok_test.status_code == 200), str(get_podcast_ok_test.content)
        res = json.loads(str(get_podcast_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_podcast_popular(self):
        singer = Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
            is_channel=True
        )
        singer.save()
        for i in range(13):
            song = Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                is_podcast=True,
                description="",
                link="test",
                view_count=i,
                singer=singer
            )
            song.save()
        get_podcast_ok_test = self.client.get('/api/web/songs/podcasts/popular', data={})
        assert (get_podcast_ok_test.status_code == 200), str(get_podcast_ok_test.content)
        res = json.loads(str(get_podcast_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Singer_Channel.objects.filter(en_name="test").delete()
        Songs.objects.filter(en_name="test").delete()

        get_podcast_ok_test = self.client.get('/api/web/songs/podcasts/popular', data={})
        assert (get_podcast_ok_test.status_code == 200), str(get_podcast_ok_test.content)
        res = json.loads(str(get_podcast_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_playlists(self):
        for i in range(13):
            Playlists(
                playlist_id=i,
                name="test",
                cover="test",
                is_active=True
            ).save()
        get_playlist_ok_test = self.client.get('/api/web/songs/playlists', data={})
        assert (get_playlist_ok_test.status_code == 200), str(get_playlist_ok_test.content)
        res = json.loads(str(get_playlist_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Playlists.objects.filter(name="test").delete()

        get_playlist_ok_test = self.client.get('/api/web/songs/playlists', data={})
        assert (get_playlist_ok_test.status_code == 200), str(get_playlist_ok_test.content)
        res = json.loads(str(get_playlist_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_playlists_all(self):
        for i in range(13):
            Playlists(
                playlist_id=i,
                name="test",
                cover="test",
                is_active=True
            ).save()
        get_playlist_ok_test = self.client.get('/api/web/songs/playlists/all', data={})
        assert (get_playlist_ok_test.status_code == 200), str(get_playlist_ok_test.content)
        res = json.loads(str(get_playlist_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 13), str(res['data'])

        Playlists.objects.filter(name="test").delete()

        get_playlist_ok_test = self.client.get('/api/web/songs/playlists/all', data={})
        assert (get_playlist_ok_test.status_code == 200), str(get_playlist_ok_test.content)
        res = json.loads(str(get_playlist_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_playlist_songs(self):
        playlist_1 = Playlists(
            playlist_id=1,
            name="test",
            cover="test",
            is_active=True
        )
        playlist_1.save()
        Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        ).save()
        for i in range(13):
            song = Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                description="",
                link="test",
                singer_id=1
            )
            song.save()
            playlist_1.songs.add(song)
        playlist_2 = Playlists(
            playlist_id=1,
            name="test",
            cover="test",
            is_active=True
        )
        playlist_2.save()
        for i in range(13):
            song = Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                description="",
                link="test",
                singer_id=1
            )
            song.save()
            playlist_2.songs.add(song)
        get_playlist_ok_test_1 = self.client.get('/api/web/songs/playlist/1', data={})
        assert (get_playlist_ok_test_1.status_code == 200), str(get_playlist_ok_test_1.content)
        res = json.loads(str(get_playlist_ok_test_1.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        get_playlist_ok_test_2 = self.client.get('/api/web/songs/playlist/1', data={})
        assert (get_playlist_ok_test_2.status_code == 200), str(get_playlist_ok_test_2.content)
        res = json.loads(str(get_playlist_ok_test_2.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Songs.objects.filter(en_name="test").delete()
        Playlists.objects.filter(name="test").delete()

        get_playlist_fail_test_1 = self.client.get('/api/web/songs/playlist/1', data={})
        assert (get_playlist_fail_test_1.status_code == 404), str(get_playlist_fail_test_1.content)

        get_playlist_fail_test_2 = self.client.get('/api/web/songs/playlist/2', data={})
        assert (get_playlist_fail_test_2.status_code == 404), str(get_playlist_fail_test_2.content)

    def test_get_songs_singers(self):
        for i in range(13):
            Singer_Channel(
                singer_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                is_active=True,
            ).save()
        get_singers_ok_test = self.client.get('/api/web/songs/singers', data={})
        assert (get_singers_ok_test.status_code == 200), str(get_singers_ok_test.content)
        res = json.loads(str(get_singers_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Singer_Channel.objects.filter(en_name="test").delete()

        get_singers_ok_test = self.client.get('/api/web/songs/singers', data={})
        assert (get_singers_ok_test.status_code == 200), str(get_singers_ok_test.content)
        res = json.loads(str(get_singers_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_songs_singers_all(self):
        for i in range(13):
            Singer_Channel(
                singer_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                is_active=True,
            ).save()
        get_singers_ok_test = self.client.get('/api/web/songs/singers/all', data={})
        assert (get_singers_ok_test.status_code == 200), str(get_singers_ok_test.content)
        res = json.loads(str(get_singers_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 13), str(res['data'])

        Singer_Channel.objects.filter(en_name="test").delete()

        get_singers_ok_test = self.client.get('/api/web/songs/singers/all', data={})
        assert (get_singers_ok_test.status_code == 200), str(get_singers_ok_test.content)
        res = json.loads(str(get_singers_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])

    def test_get_songs_single_singer(self):
        Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        ).save()
        Singer_Channel(
            singer_id=2,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        ).save()
        for i in range(13):
            Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                is_podcast=True,
                description="",
                link="test",
                view_count=i,
                singer_id=1
            ).save()
        for i in range(13):
            Songs(
                song_id=i + 13,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                is_podcast=True,
                description="",
                link="test",
                view_count=i,
                singer_id=2
            ).save()
        get_song_ok_test = self.client.get('/api/web/songs/singers/1', data={})
        assert (get_song_ok_test.status_code == 200), str(get_song_ok_test.content)
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        get_song_ok_test_2 = self.client.get('/api/web/songs/singers/1', data={})
        assert (get_song_ok_test_2.status_code == 200), str(get_song_ok_test_2.content)
        res = json.loads(str(get_song_ok_test_2.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Songs.objects.filter(en_name="test").delete()
        Singer_Channel.objects.filter(en_name="test").delete()

        get_song_fail_test = self.client.get('/api/web/songs/singers/1', data={})
        assert (get_song_fail_test.status_code == 404), str(get_song_fail_test.content)

        get_song_fail_test = self.client.get('/api/web/songs/singers/2', data={})
        assert (get_song_fail_test.status_code == 404), str(get_song_fail_test.content)

    def test_get_songs_channels(self):
        for i in range(13):
            Singer_Channel(
                singer_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                is_active=True,
                is_channel=True
            ).save()
        get_channels_ok_test = self.client.get('/api/web/songs/channels', data={})
        assert (get_channels_ok_test.status_code == 200), str(get_channels_ok_test.content)
        res = json.loads(str(get_channels_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Singer_Channel.objects.filter(en_name="test").delete()

        get_channels_fail_test = self.client.get('/api/web/songs/channels', data={})
        assert (get_channels_fail_test.status_code == 404), str(get_channels_fail_test.content)

    def test_get_songs_channels_all(self):
        for i in range(13):
            Singer_Channel(
                singer_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                is_active=True,
                is_channel=True
            ).save()
        get_channels_ok_test = self.client.get('/api/web/songs/channels/all', data={})
        assert (get_channels_ok_test.status_code == 200), str(get_channels_ok_test.content)
        res = json.loads(str(get_channels_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 13), str(res['data'])

        Singer_Channel.objects.filter(en_name="test").delete()

        get_channels_fail_test = self.client.get('/api/web/songs/channels/all', data={})
        assert (get_channels_fail_test.status_code == 404), str(get_channels_fail_test.content)

    def test_get_songs_single_channel(self):
        Singer_Channel(
            singer_id=5,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
            is_channel=True
        ).save()
        Singer_Channel(
            singer_id=7,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
            is_channel=True
        ).save()
        for i in range(13):
            Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                is_podcast=True,
                description="",
                link="test",
                view_count=i,
                singer_id=5,

            ).save()
        for i in range(13):
            Songs(
                song_id=i + 13,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                is_active_image=True,
                is_active_link=True,
                is_podcast=True,
                description="",
                link="test",
                view_count=i,
                singer_id=7
            ).save()
        get_song_ok_test = self.client.get('/api/web/songs/channel/5', data={})
        assert (get_song_ok_test.status_code == 200), str(get_song_ok_test.content)
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        get_song_ok_test_2 = self.client.get('/api/web/songs/channel/7', data={})
        assert (get_song_ok_test_2.status_code == 200), str(get_song_ok_test_2.content)
        res = json.loads(str(get_song_ok_test_2.content.decode("utf8")))
        assert (res['data'].__len__() == 10), str(res['data'])

        Songs.objects.filter(en_name="test").delete()
        Singer_Channel.objects.filter(en_name="test").delete()

        get_song_fail_test = self.client.get('/api/web/songs/singers/5', data={})
        assert (get_song_fail_test.status_code == 404), str(get_song_fail_test.content)

        get_song_fail_test = self.client.get('/api/web/songs/singers/7', data={})
        assert (get_song_fail_test.status_code == 404), str(get_song_fail_test.content)

    def test_get_ads(self):
        for i in range(10):
            ad = Ads(
                ad_id=i,
                image_url="test",
                is_active=True,
                is_video_ads=False
            )
            ad.save()
        get_ads_ok_test = self.client.get('/api/web/songs/ads', data={})
        assert (get_ads_ok_test.status_code == 200), str(get_ads_ok_test.content)
        res = json.loads(str(get_ads_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 3), str(res['data'])

        Ads.objects.filter(image_url="test").delete()

        get_ads_ok_test = self.client.get('/api/web/songs/ads', data={})
        assert (get_ads_ok_test.status_code == 200), str(get_ads_ok_test.content)
        res = json.loads(str(get_ads_ok_test.content.decode("utf8")))
        assert (res['data'].__len__() == 0), str(res['data'])


##############################
'''unit tests'''


class UniTests(TestCase):
    def test_get_new_videos(self):
        for i in range(10):
            create_category()
            create_video(i,
                         is_active_link=True if i < 5 else False,
                         is_active_image=True if i > 3 else False,
                         is_childish=False)
        get_video = Util_Web.get_new_videos()
        self.assert_(list(get_video).__len__() == 1, get_video)

    def test_get_most_visited_videos(self):
        create_category()
        actor = VideoActors(
            actor_id=1,
            fa_name='test',
            en_name='test',
            avatar='test',
            is_active=True
        )
        actor.save()
        for i in range(10):
            video = Videos(
                video_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                summary="test",
                director="test",
                category_id=1,
                link="test",
                description="test",
                is_active_image=True if i > 3 else False,
                is_active_link=True if i < 5 else False,
            )
            video.save()
            actor.videos.add(video)
        get_video = Util_Web.get_most_visited_videos()
        self.assert_(list(get_video).__len__() == 1, get_video)

    def test_get_video(self):
        create_category()
        vid = Videos(
            video_id=1,
            length=1,
            en_name="test",
            fa_name="test",
            category_id=1,
            is_active_image=False,
            is_active_link=False,
            image_link="test"
        )
        vid.save()
        get_vid = Util_Web.get_video(vid)
        self.assert_(get_vid, get_vid)

    def test_get_category(self):
        cat = VideoCategory(
            category_id=1,
            image_link="test",
            is_active=False,
            title="test",
        )
        cat.save()
        get_category = Util_Web.Get_category(cat)
        self.assert_(get_category, get_category)

    def test_get_song(self):
        create_singer(singer_id=1)
        song = Songs(
            song_id=1,
            image_link="test",
            fa_name="test",
            en_name="test",
            length=2,
            is_active_link=True,
            singer_id=1
        )
        song.save()
        get_song = Util_Web.get_song(song)
        self.assert_(get_song, get_song)

    def test_get_song_singers(self):
        create_singer(singer_id=1)
        create_singer(singer_id=2, is_channel=True)
        create_singer(singer_id=3, is_active=False)
        Songs(
            song_id=1,
            image_link="test",
            fa_name="test",
            en_name="test",
            length=2,
            is_active_link=True,
            singer_id=1
        ).save()
        Songs(
            song_id=2,
            image_link="test",
            fa_name="test",
            en_name="test",
            length=2,
            is_active_link=True,
            singer_id=2,
        ).save()
        Songs(
            song_id=3,
            image_link="test",
            fa_name="test",
            en_name="test",
            length=2,
            is_active_link=True,
            singer_id=3
        ).save()
        get_singer = Util_Web.get_song_singers()
        self.assert_(list(get_singer).__len__() == 1, list(get_singer))

    def test_get_latest_songs(self):
        create_singer(1)
        for i in range(10):
            create_song(
                i,
                is_active_image=True if i < 5 else False,
                is_active_link=True if i > 3 else False,
                is_childish=False,
                singer_id=1
            )
        get_song = Util_Web.get_latest_songs()
        self.assert_(list(get_song).__len__() == 1, get_song)
        create_singer(1)
        for i in range(12):
            create_song(
                i,
                is_active_image=True,
                is_active_link=True,
                is_childish=False,
                singer_id=1
            )
        get_song = Util_Web.get_latest_songs()
        self.assert_(list(get_song).__len__() == 10, get_song)

    def test_get_popular_songs(self):
        create_singer(1)
        for i in range(10):
            create_song(
                i,
                is_active_image=True if i < 5 else False,
                is_active_link=True if i > 3 else False,
                is_childish=False,
                singer_id=1
            )
        get_song = Util_Web.get_latest_songs()
        self.assert_(list(get_song).__len__() == 1, get_song)
        for i in range(12):
            create_singer(1)
            create_song(
                i,
                is_active_image=True,
                is_active_link=True,
                is_childish=False,
                singer_id=1
            )
        get_song = Util_Web.get_latest_songs()
        self.assert_(list(get_song).__len__() == 10, get_song)

    def test_get_singer_songs(self):
        Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        ).save()
        Singer_Channel(
            singer_id=2,
            fa_name="test",
            en_name="test",
            image_link="test",
            is_active=True,
        ).save()
        for i in range(12):
            create_song(
                i,
                is_active_image=True,
                is_active_link=True,
                is_childish=False,
                singer_id=1
            )
        get_song = Util_Web.get_singer_songs(singer_id=1)
        self.assert_(list(get_song).__len__() == 10, get_song)
        for i in range(10):
            create_song(
                i,
                is_active_image=True if i < 5 else False,
                is_active_link=True if i > 3 else False,
                is_childish=False,
                singer_id=2
            )
        get_song = Util_Web.get_singer_songs(singer_id=2)
        self.assert_(list(get_song).__len__() == 1, get_song)
        Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            image_link="test",
        ).save()
        for i in range(12):
            create_song(
                i,
                is_active_image=True,
                is_active_link=True,
                is_childish=False,
                singer_id=1
            )
        get_song = Util_Web.get_singer_songs(singer_id=2)
        self.assert_(not list(get_song), get_song)
    
    def test_get_all_singers(self):
        for i in range(13):
            create_singer(i,
                          is_active=True if i < 5 else False,
                          is_channel=False if i > 3 else True,
                          )
        get_singer = Util_Web.get_all_singers()
        self.assert_( list(get_singer).__len__() == 1, get_singer)
        for i in range(13):
            create_singer(i)
        get_singer = Util_Web.get_all_singers()
        self.assert_( list(get_singer).__len__() == 10, get_singer)

    def test_get_latest_podcasts(self):
        create_singer(1)
        for i in range(10):
            create_song(
                song_id=i,
                is_active_image=True if i < 5 else False,
                is_active_link=True if i > 3 else False,
                is_childish=False,
                singer_id=1,
                is_podcast=True
            )
        get_podcast = Util_Web.get_latest_podcasts()
        self.assertTrue(list(get_podcast).__len__() == 1, get_podcast)
        Singer_Channel(
            singer_id=1,
            is_channel=True,
            is_active=True,
            en_name="test",
            fa_name="test",
            image_link=""
        ).save()
        for i in range(12):
            Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=1,
                description="",
                is_active_link=True,
                is_active_image=True,
                singer_id=1,
                is_childish=False,
                is_podcast=True,
                view_count=1,
                min_age=3
            ).save()
        get_latest_podcasts = Util_Web.get_latest_podcasts()
        self.assert_(list(get_latest_podcasts).__len__() == 10, list(get_latest_podcasts))

    def test_get_three_ads(self):
        for i in range(10):
            Ads(
                ad_id=i,
                is_active=True if i > 3 else False,
                is_video_ads=False if i < 5 else True,
            ).save()
        get_ads = util.get_three_ads()
        self.assert_(list(get_ads).__len__() == 0, get_ads)
        for i in range(10):
            Ads(
                ad_id=i,
                is_active=True,
                is_video_ads=False,
            ).save()
        get_ads = util.get_three_ads()
        self.assert_(list(get_ads).__len__() == 3, get_ads)

    def test_get_channel_all(self):
        for i in range(13):
            Singer_Channel(
                singer_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                is_active=True if i > 3 else False,
                is_channel=True if i < 5 else False,
            ).save()

        get_channels = Util_Web.get_channel_all()
        self.assert_(list(get_channels).__len__() == 1, get_channels)

        Singer_Channel.objects.filter(en_name="test").delete()
        for i in range(13):
            Singer_Channel(
                singer_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                is_active=True,
                is_channel=True,
            ).save()
        get_channels = Util_Web.get_channel_all()
        self.assert_(list(get_channels).__len__() == 13, get_channels)

    def test_get_channels(self):
        for i in range(13):
            Singer_Channel(
                singer_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                is_active=True if i > 3 else False,
                is_channel=True if i < 5 else False,
            ).save()

        get_channels = Util_Web.get_channel_all()
        self.assert_(list(get_channels).__len__() == 1, get_channels)
        Singer_Channel.objects.filter(en_name="test").delete()
        for i in range(13):
            Singer_Channel(
                singer_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                is_active=True,
                is_channel=True,
            ).save()
        get_channels = Util_Web.get_channels()
        self.assert_(list(get_channels).__len__() == 10, get_channels)

    def test_get_all_singers(self):
        for i in range(13):
            Singer_Channel(
                singer_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                is_active=True if i > 3 else False,
                is_channel=False if i < 5 else True,
            ).save()
        get_singers = Util_Web.get_all_singers()
        self.assert_(list(get_singers).__len__() == 1, get_singers)

    def test_get_all_playlists(self):
        for i in range(1, 13):
            Playlists(
                playlist_id=i,
                cover="test",
                is_active=False if i % 11 else True
            ).save()
        get_playlists = Util_Web.get_all_playlists()
        self.assert_(list(get_playlists).__len__() == 1, get_playlists)

    def test_get_channel_songs(self):
        # create_singer(1, is_active=True, is_channel=True)
        Singer_Channel(
            singer_id=1,
            is_channel=True,
            is_active=True,
            en_name="test",
            fa_name="test",
            image_link=""
        ).save()
        for i in range(12):
            Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=1,
                description="",
                is_active_link=True,
                is_active_image=True,
                singer_id=1,
                is_childish=False,
                is_podcast=False,
                view_count=1,
                min_age=3
            ).save()
        get_channel_songs = Util_Web.get_channel_songs(channel_id=1)
        self.assert_(list(get_channel_songs).__len__() == 10, list(get_channel_songs))

    def test_search(self):
        Singer_Channel(
            singer_id=1,
            fa_name="test",
            en_name="test",
            is_active=True,
            image_link="test",
        ).save()
        for i in range(1, 12):
            Songs(
                song_id=i,
                fa_name="test",
                is_active_image=True,
                is_active_link=True,
                is_podcast=False,
                description="test" if i % 11 else "key",
                singer_id=1,
                image_link="test",
                length=1
            ).save()
        create_category()
        for i in range(1, 13):
            Videos(
                video_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=0,
                summary="test",
                director="test",
                category_id=1,
                link="test",
                description="test" if i % 11 else "key",
                is_active_image=True,
                is_active_link=True,
            ).save()
        get_search = Util_Web.search(search="key")
        self.assert_(list(get_search['song']).__len__() == 1, list(get_search['song']))
        self.assert_(list(get_search['video']).__len__() == 1, list(get_search['video']))

    def test_get_popular_podcasts(self):
        Singer_Channel(
            singer_id=1,
            is_channel=True,
            is_active=True,
            en_name="test",
            fa_name="test",
            image_link=""
        ).save()
        for i in range(12):
            Songs(
                song_id=i,
                fa_name="test",
                en_name="test",
                image_link="test",
                length=1,
                description="",
                is_active_link=True,
                is_active_image=True,
                singer_id=1,
                is_childish=False,
                is_podcast=True,
                view_count=1,
                min_age=3
            ).save()
        get_popular_podcasts = Util_Web.get_popular_podcasts()
        self.assert_(list(get_popular_podcasts).__len__() == 10, list(get_popular_podcasts))



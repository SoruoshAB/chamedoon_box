import json
from datetime import datetime, timedelta

from django.test import TestCase
from django.test import Client

from accounts.util import Util_Accounts
from apiApp.models import *
from apiWeb.models import *

from apiApp.util import Util_App

from apiApp.models import Videos, VideoImages, VideoCategory, Songs, Singer_Channel, Playlists


def create_token():
    access_token_content = {
        "device": "android",
        "user_id": 1
    }
    refresh_token = Util_Accounts().generate_refresh_token(datetime.utcnow() + timedelta(days=100),
                                                           device=access_token_content["device"],
                                                           user_id=access_token_content["user_id"])
    access_token = Util_Accounts().generate_access_token(datetime.utcnow() + timedelta(days=30),
                                                         device=access_token_content["device"],
                                                         user_id=access_token_content["user_id"],
                                                         refresh_token=refresh_token)
    return refresh_token, access_token


def create_video(Id, is_active_link=True, is_active_image=True, is_childish=False, category_id=1, view_count=0):
    video = Videos(
        video_id=Id,
        fa_name="test",
        en_name="test",
        image_link="test",
        description="",
        length=0,
        summary="Test",
        director="test",
        category_id=category_id,
        link="Test",
        is_active_image=is_active_link,
        is_active_link=is_active_image,
        is_childish=is_childish,
        view_count=view_count
    )
    video.save()
    return video


def create_Category(Id, is_active=True):
    VideoCategory(
        category_id=Id,
        is_active=is_active,
        image_link="test",
        title="test").save()


def create_singer_channel(Id, is_channel=False, is_active=True):
    singer = Singer_Channel(
        singer_id=Id,
        fa_name="test",
        en_name="test",
        image_link="test",
        is_channel=is_channel,
        is_active=is_active,
    )
    singer.save()
    return singer


def create_song(Id, singer, is_active_link=True, is_active_image=True, is_podcast=False, is_childish=False):
    song = Songs(
        song_id=Id,
        fa_name="test",
        en_name="test",
        image_link="test",
        length=0,
        is_active_image=is_active_image,
        is_active_link=is_active_link,
        description="",
        link="test",
        singer=singer,
        is_podcast=is_podcast,
        is_childish=is_childish
    )
    song.save()
    return song


def create_ads(Id, is_video_ads=False, video=None, is_active=True):
    Ads(
        ad_id=Id,
        image_url="test",
        click_url="test",
        video=video,
        is_video_ads=is_video_ads,
        is_active=is_active,
    ).save()


class HomeTests(TestCase):
    def test_home_view(self):
        # create a category
        create_Category(1)

        # create 12th video
        video = list(map(lambda Id: create_video(Id + 1), range(12)))

        # create a slider video
        slider_video = SliderVideo(
            slider_id=1,
            video=video[0],
            image_link="test",
            is_show=True,
            is_childish=False,
            is_active=True,
        )
        slider_video.save()

        # create a slider home video
        SliderHome(
            slider_id=1,
            type=0,
            VideoSlider=slider_video,
            SongSlider=None,
            AdsSlider=None,
            name="test",
        ).save()

        # create a singer
        singer = create_singer_channel(1)

        # create a channel
        channel = create_singer_channel(2, True)

        # create 12th songs
        song = list(map(lambda Id: create_song(Id + 1, singer), range(12)))

        # create 12th podcaste
        podcast = list(map(lambda Id: create_song(Id + 1, channel, is_podcast=True), range(12, 24)))

        # create a slider song
        slider_song = SliderSong(
            slider_id=1,
            image_link="test",
            lyric="test",
            release_date="test",
            tarane="test",
            tuning="test",
            is_show=True,
            Song=song[0],
            is_active=True,
        )
        slider_song.save()

        # create a slider home song
        SliderHome(
            slider_id=2,
            type=1,
            VideoSlider=None,
            SongSlider=slider_song,
            AdsSlider=None,
            name="test",
        ).save()
        # create 5th Ads
        ads = list(map(lambda Id: create_ads(Id), range(5)))

        # create a slider ads
        slider_ads = SliderAds(
            slider_id=1,
            image_url="test",
            click_url="test",
            title="test",
            is_active=True,
        )
        slider_ads.save()

        # create a slider home ads
        SliderHome(
            slider_id=3,
            type=2,
            VideoSlider=None,
            SongSlider=None,
            AdsSlider=slider_ads,
            name="test",
        ).save()

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_home_ok_test = self.client.get('/api/app/Home', data={}, **header)
        get_home_without_authorization = self.client.get('/api/app/Home', data={})
        res = json.loads(str(get_home_ok_test.content.decode("utf8")))

        assert (get_home_ok_test.status_code == 200), str(get_home_ok_test.content)
        assert (get_home_without_authorization.status_code == 401), str(get_home_without_authorization.content)
        assert (res['data']["slider"].__len__() == 3), str(res['data']["slider"])
        assert (res['data']["slider"]["slider_video"].__len__() == 1), str(res['data']["slider"]["slider_video"])
        assert (res['data']["slider"]["slider_song"].__len__() == 1), str(res['data']["slider"]["slider_song"])
        assert (res['data']["slider"]["slider_ads"].__len__() == 1), str(res['data']["slider"]["slider_ads"])
        assert (res['data']["newest_video"].__len__() == 10), str(res['data']["newest_video"])
        assert (res['data']["newest_song"].__len__() == 10), str(res['data']["newest_song"])
        assert (res['data']["newest_podcast"].__len__() == 10), str(res['data']["newest_podcast"])
        assert (res['data']["ads"].__len__() == 3), str(res['data']["ads"])
        VideoCategory.objects.all().delete()
        Singer_Channel.objects.all().delete()
        Ads.objects.all().delete()
        SliderAds.objects.all().delete()
        get_home_ok_test = self.client.get('/api/app/Home', data={}, **header)
        res = json.loads(str(get_home_ok_test.content.decode("utf8")))

        assert (get_home_ok_test.status_code == 200), str(get_home_ok_test.content)
        assert (get_home_without_authorization.status_code == 401), str(get_home_without_authorization.content)
        assert (res['data']["slider"].__len__() == 3), str(res['data']["slider"])
        assert (res['data']["slider"]["slider_video"].__len__() == 0), str(res['data']["slider"]["slider_video"])
        assert (res['data']["slider"]["slider_song"].__len__() == 0), str(res['data']["slider"]["slider_song"])
        assert (res['data']["slider"]["slider_ads"].__len__() == 0), str(res['data']["slider"]["slider_ads"])
        assert (res['data']["newest_video"].__len__() == 0), str(res['data']["newest_video"])
        assert (res['data']["newest_song"].__len__() == 0), str(res['data']["newest_song"])
        assert (res['data']["newest_podcast"].__len__() == 0), str(res['data']["newest_podcast"])
        assert (res['data']["ads"].__len__() == 0), str(res['data']["ads"])

    def test_slider_video(self):
        create_Category(1)

        for i in range(4):
            i += 1
            video = create_video(i,
                                 is_active_link=True if i in (1, 2, 3) else False,
                                 is_active_image=True if i in (2, 3, 4) else False
                                 )
            slider_video = SliderVideo(
                slider_id=i,
                video=video,
                image_link="test",
                is_show=True,
                is_childish=False,
                is_active=True if i != 2 else False
            )
            slider_video.save()

        slider = Util_App.get_slider_video(False)
        assert (slider.__len__() == 1), str(slider)

    def test_slider_song(self):
        singer = create_singer_channel(1)
        channel = create_singer_channel(2, is_channel=True)
        for i in range(5):
            i += 1
            song = create_song(i, singer=singer if i != 3 else channel,
                               is_active_image=True if i == 1 else False,
                               is_active_link=True if i != 5 else False,
                               is_podcast=True if i == 3 else False)
            slider_song = SliderSong(
                slider_id=i,
                image_link="test",
                lyric="test",
                release_date="test",
                tarane="test",
                tuning="test",
                is_show=True,
                Song=song,
                is_active=True if i != 4 else False,
            )
            slider_song.save()

        slider = Util_App.get_slider_song()
        assert (slider.__len__() == 3), str(slider)

    def test_slider_ads(self):
        for i in range(2):
            i += 1
            slider_ads = SliderAds(
                slider_id=i,
                image_url="test",
                click_url="test",
                title="test",
                is_active=True if i == 1 else False
            )
            slider_ads.save()
            SliderHome(
                slider_id=i,
                type=2,
                VideoSlider=None,
                SongSlider=None,
                AdsSlider=slider_ads,
                name="test",
            ).save()
        slider = Util_App.get_home_slider_ads()
        assert (slider.__len__() == 1), str(slider)

    def test_new_video(self):
        # create cat
        create_Category(1)

        for i in range(5):
            i += 1
            video = create_video(i,
                                 is_active_link=True if i in (1, 2, 3) else False,
                                 is_active_image=True if i in (2, 3, 4) else False,
                                 is_childish=True if i == 3 else False
                                 )
        video = list(Util_App.get_new_videos())
        assert (video.__len__() == 1), str(video)

    def test_new_song(self):
        for i in range(6):
            i += 1
            singer = create_singer_channel(i,
                                           is_active=True if i != 6 else False,
                                           is_channel=False if i != 3 else True
                                           )
            create_song(i,
                        singer=singer,
                        is_active_image=True if i != 4 else False,
                        is_active_link=True if i != 2 else False,
                        is_podcast=True if i == 3 else False,
                        is_childish=True if i == 5 else False,
                        )

        song = list(Util_App.get_new_songs())
        assert (song.__len__() == 1), str(song)

    def test_new_podcast(self):
        for i in range(6):
            i += 1
            channel = create_singer_channel(i,
                                            is_active=True if i != 6 else False,
                                            is_channel=True if i != 5 else False
                                            )
            create_song(i,
                        singer=channel,
                        is_active_image=True if i != 3 else False,
                        is_active_link=True if i != 2 else False,
                        is_podcast=True if i != 4 else False,
                        )
        song = list(Util_App.get_new_podcast())
        assert (song.__len__() == 1), str(song)


class childTests(TestCase):
    def test_child_view(self):
        # create a category
        create_Category(1)

        # create 22th videos
        video = list(map(lambda Id: create_video(Id + 1, is_childish=True), range(22)))

        # create a slider child video
        slider_video = SliderVideo(
            slider_id=1,
            video=video[0],
            image_link="test",
            is_show=True,
            is_childish=True,
            is_active=True,
        )
        slider_video.save()

        # create 3th images video
        for i in range(3):
            i += 1
            image = VideoImages(
                image_id=i,
                video=video[0],
                link="test",
                is_sticker=False,
                name="test",
                is_active=True,
            ).save()

        # create a singer
        singer = create_singer_channel(1)

        # create 22th songs
        song = list(map(lambda Id: create_song(Id + 1, singer, is_childish=True), range(22)))

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_child_ok_test = self.client.get('/api/app/child', data={}, **header)
        get_child_without_authorization = self.client.get('/api/app/child', data={})
        res = json.loads(str(get_child_ok_test.content.decode("utf8")))

        assert (get_child_ok_test.status_code == 200), str(get_child_ok_test.content)
        assert (get_child_without_authorization.status_code == 401), str(get_child_without_authorization.content)
        assert (res['data']["slider"].__len__() == 1), str(res['data']["slider"])
        assert (res['data']["animations"].__len__() == 21), str(res['data']["animations"])
        assert (res['data']["animations_image"].__len__() == 12), str(res['data']["animations_image"])
        assert (res['data']["song_child"].__len__() == 21), str(res['data']["song_child"])

        Videos.objects.filter(fa_name="test").delete()
        Singer_Channel.objects.filter(en_name="test").delete()

        get_child_delete_test = self.client.get('/api/app/child', data={}, **header)
        res = json.loads(str(get_child_delete_test.content.decode("utf8")))
        assert (get_child_ok_test.status_code == 200), str(get_child_ok_test.content)
        assert (res['data']["slider"].__len__() == 0), str(res['data']["slider"])
        assert (res['data']["animations"].__len__() == 0), str(res['data']["animations"])
        assert (res['data']["animations_image"].__len__() == 0), str(res['data']["animations_image"])
        assert (res['data']["song_child"].__len__() == 0), str(res['data']["song_child"])

    def test_slider_child(self):
        # create a category
        create_Category(1)

        for i in range(5):
            i += 1

            # create 22th videos
            video = create_video(i, is_childish=True if i != 2 else False,
                                 is_active_link=True if i != 3 else False,
                                 )

            # create a slider child video
            slider_video = SliderVideo(
                slider_id=i,
                video=video,
                image_link="test",
                is_show=True if i != 4 else False,
                is_childish=True if i != 2 else False,
                is_active=True if i != 5 else False
            )
            slider_video.save()

        # create 3th images video
        for i in range(5):
            i += 1
            VideoImages(
                image_id=i,
                video=Videos.objects.first(),
                link="test",
                is_sticker=False if i != 4 else True,
                name="test",
                is_active=True if i != 5 else False,
            ).save()
        slider = list(Util_App.get_slider_video_child())
        assert (slider.__len__() == 1), str(slider)
        assert (slider[0]["images"].__len__() == 3), str(slider[0]["images"])
        assert (slider[0]["images"][0]["image_id"] == 3), str(slider[0]["images"])

    def test_new_videos_child(self):
        # create a category
        create_Category(1)

        for i in range(4):
            i += 1
            create_video(i,
                         is_childish=True if i != 2 else False,
                         is_active_link=True if i != 3 else False,
                         is_active_image=True if i != 4 else False,
                         )
        video = list(Util_App.get_new_videos_child())
        assert (video.__len__() == 1), str(video)
        video_image = list(Util_App.get_new_videos_child(image=False))
        assert (video_image.__len__() == 1), str(video_image)
        assert (video != video_image), str(video_image)

    def test_new_songs_child(self):
        singer = create_singer_channel(1)

        for i in range(4):
            i += 1
            create_song(i, singer,
                        is_childish=True if i != 2 else False,
                        is_active_image=True if i != 3 else False,
                        is_active_link=True if i != 4 else False
                        )

        song = list(Util_App.get_new_songs_child())
        assert (song.__len__() == 1), str(song)


class SearchTests(TestCase):
    def test_child_view(self):
        # create a category
        create_Category(1)

        # create a video
        video = list(map(lambda Id: create_video(Id + 1), range(10)))

        # create a singer
        singer = create_singer_channel(1)

        # create a songs
        song = list(map(lambda Id: create_song(Id + 1, singer), range(10)))

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_search_ok_test = self.client.get('/api/app/search', data={"search": "test"}, **header)
        get_search_without_authorization = self.client.get('/api/app/search', data={"search": "test"})
        res = json.loads(str(get_search_ok_test.content.decode("utf8")))

        assert (get_search_ok_test.status_code == 200), str(get_search_ok_test.content)
        assert (get_search_without_authorization.status_code == 401), str(get_search_without_authorization.content)

        assert (res['data']["video"].__len__() == 10), str(res['data']["video"])
        assert (res['data']["song"].__len__() == 10), str(res['data']["song"])

        VideoCategory.objects.filter(category_id=1).delete()
        Singer_Channel.objects.filter(en_name="test").delete()

        get_search_ok_test = self.client.get('/api/app/search', data={"search": "test"}, **header)
        res = json.loads(str(get_search_ok_test.content.decode("utf8")))
        assert (res['data']["video"].__len__() == 0), str(res['data']["video"])
        assert (res['data']["song"].__len__() == 0), str(res['data']["song"])


class MusicTests(TestCase):
    def test_music_view(self):
        # create a singer
        singer = create_singer_channel(1)

        # create a channel
        channel = create_singer_channel(2, True)

        # create 12th songs
        song = list(map(lambda Id: create_song(Id + 1, singer), range(12)))

        # create 12th podcaste
        podcast = list(map(lambda Id: create_song(Id + 1, channel, is_podcast=True), range(12, 24)))

        # create a slider song
        slider_song = SliderSong(
            slider_id=1,
            image_link="test",
            lyric="test",
            release_date="test",
            tarane="test",
            tuning="test",
            is_show=True,
            Song=song[0],
            is_active=True,
        )
        slider_song.save()

        # creat a playlist
        playlist = Playlists(
            playlist_id=1,
            name="test",
            cover="test",
            is_active=True,
        )
        playlist.save()
        playlist.songs.add(song[0])

        # create 5th Ads
        ads = list(map(lambda Id: create_ads(Id), range(5)))

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_music_ok_test = self.client.get('/api/app/Songs', data={}, **header)
        get_music_without_authorization = self.client.get('/api/app/Songs', data={})
        res = json.loads(str(get_music_ok_test.content.decode("utf8")))

        assert (get_music_ok_test.status_code == 200), str(get_music_ok_test.content)
        assert (get_music_without_authorization.status_code == 401), str(get_music_without_authorization.content)
        assert (res['data']["slider_song"].__len__() == 1), str(res['data']["slider_song"])
        assert (res['data']["play_list"].__len__() == 1), str(res['data']["play_list"])
        assert (res['data']["singer"].__len__() == 1), str(res['data']["singer"])
        assert (res['data']["newest_song"].__len__() == 10), str(res['data']["newest_song"])
        assert (res['data']["newest_channel"].__len__() == 1), str(res['data']["newest_channel"])
        assert (res['data']["newest_podcast"].__len__() == 10), str(res['data']["newest_podcast"])
        assert (res['data']["ads"].__len__() == 3), str(res['data']["ads"])

        Singer_Channel.objects.all().delete()
        Ads.objects.all().delete()
        Playlists.objects.filter(name="test").delete()
        get_music_ok_test = self.client.get('/api/app/Songs', data={}, **header)
        res = json.loads(str(get_music_ok_test.content.decode("utf8")))

        assert (get_music_ok_test.status_code == 200), str(get_music_ok_test.content)
        assert (res['data']["slider_song"].__len__() == 0), str(res['data']["slider_song"])
        assert (res['data']["play_list"].__len__() == 0), str(res['data']["play_list"])
        assert (res['data']["singer"].__len__() == 0), str(res['data']["singer"])
        assert (res['data']["newest_song"].__len__() == 0), str(res['data']["newest_song"])
        assert (res['data']["newest_channel"].__len__() == 0), str(res['data']["newest_channel"])
        assert (res['data']["newest_podcast"].__len__() == 0), str(res['data']["newest_podcast"])
        assert (res['data']["ads"].__len__() == 0), str(res['data']["ads"])

    def test_get_slider_song(self):
        # create a singer
        singer = create_singer_channel(1)

        for i in range(5):
            i += 1
            song = create_song(i, singer,
                               is_active_link=True if i != 2 else False,
                               is_active_image=True if i != 3 else False,
                               )

            slider_song = SliderSong(
                slider_id=i,
                image_link="test",
                lyric="test",
                release_date="test",
                tarane="test",
                tuning="test",
                is_show=True if i != 4 else False,
                Song=song,
                is_active=True if i != 5 else False,
            )
            slider_song.save()

        slider = Util_App.get_slider_song()

        assert (slider.__len__() == 2), str(slider)

    def test_get_play_list(self):

        # create a singer
        singer = create_singer_channel(1)

        for i in range(4):
            i += 1
            song = create_song(i, singer,
                               is_active_link=True if i != 2 else False,
                               is_active_image=True if i != 3 else False,
                               )
            playlist = Playlists(
                playlist_id=i,
                name="test",
                cover="test",
                is_active=True if i != 4 else False,
            )
            playlist.save()
            playlist.songs.add(song)

        playlist = list(Util_App.get_play_list())
        assert (playlist.__len__() == 1), str(playlist)

    def test_get_new_singer(self):
        for i in range(5):
            i += 1
            singer = create_singer_channel(i,
                                           is_channel=True if i != 2 else False,
                                           is_active=True if i != 3 else False)
            song = create_song(i, singer,
                               is_active_link=True if i != 4 else False,
                               is_active_image=True if i != 5 else False,
                               )

        singer = list(Util_App.get_new_singer())
        assert (singer.__len__() == 1), str(singer)

    def test_get_new_channel(self):
        for i in range(6):
            i += 1
            channel = create_singer_channel(i,
                                            is_channel=False if i != 2 else True,
                                            is_active=True if i != 3 else False)
            song = create_song(i, channel,
                               is_active_link=True if i != 4 else False,
                               is_active_image=True if i != 5 else False,
                               is_podcast=True if i != 6 else False
                               )

        channel = list(Util_App.get_new_channel())
        assert (channel.__len__() == 1), str(channel)


class AllSongTests(TestCase):
    def test_get_all_songs_view(self):
        # create a singer
        singer = create_singer_channel(1)

        # create a channel
        channel = create_singer_channel(2, True)

        # create 12th songs
        song = list(map(lambda Id: create_song(Id + 1, singer), range(12)))

        # create 12th podcaste
        podcast = list(map(lambda Id: create_song(Id + 1, channel, is_podcast=True), range(12, 24)))

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_song_ok_test = self.client.get('/api/app/AllSongs/1', data={}, **header)
        get_song_without_authorization = self.client.get('/api/app/AllSongs/1', data={})
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))

        assert (get_song_ok_test.status_code == 200), str(get_song_ok_test.content)
        assert (get_song_without_authorization.status_code == 401), str(get_song_without_authorization.content)

        assert (res['data']["songs"].__len__() == 10), str(res['data']["songs"])

        get_song_ok_test = self.client.get('/api/app/AllSongs/2', data={}, **header)
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))

        assert (res['data']["songs"].__len__() == 2), str(res['data']["songs"])

    def test_get_all_channel_view(self):
        # create 12th channel
        channel = list(map(lambda Id: create_singer_channel(Id + 1, True), range(12)))

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_channel_ok_test = self.client.get('/api/app/AllChannel/1', data={}, **header)
        get_channel_without_authorization = self.client.get('/api/app/AllChannel/1', data={})
        res = json.loads(str(get_channel_ok_test.content.decode("utf8")))

        assert (get_channel_ok_test.status_code == 200), str(get_channel_ok_test.content)
        assert (get_channel_without_authorization.status_code == 401), str(get_channel_without_authorization.content)

        assert (res['data']["channels"].__len__() == 10), str(res['data']["channels"])

        get_song_ok_test = self.client.get('/api/app/AllChannel/2', data={}, **header)
        res = json.loads(str(get_song_ok_test.content.decode("utf8")))

        assert (res['data']["channels"].__len__() == 2), str(res['data']["channels"])

    def test_get_all_podcast_view(self):
        # create a singer
        singer = create_singer_channel(1)

        # create a channel
        channel = create_singer_channel(2, True)

        # create 12th songs
        song = list(map(lambda Id: create_song(Id + 1, singer), range(12)))

        # create 12th podcaste
        podcast = list(map(lambda Id: create_song(Id + 1, channel, is_podcast=True), range(12, 24)))

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_podcast_ok_test = self.client.get('/api/app/AllPodcast/1', data={}, **header)
        get_podcast_without_authorization = self.client.get('/api/app/AllPodcast/1', data={})
        res = json.loads(str(get_podcast_ok_test.content.decode("utf8")))

        assert (get_podcast_ok_test.status_code == 200), str(get_podcast_ok_test.content)
        assert (get_podcast_without_authorization.status_code == 401), str(get_podcast_without_authorization.content)

        assert (res['data']["podcasts"].__len__() == 10), str(res['data']["podcasts"])

        get_podcast_ok_test = self.client.get('/api/app/AllPodcast/2', data={}, **header)
        res = json.loads(str(get_podcast_ok_test.content.decode("utf8")))

        assert (res['data']["podcasts"].__len__() == 2), str(res['data']["podcasts"])

    def test_get_all_singer_view(self):
        # create 12th singer
        for i in range(15):
            i += 1
            singer = create_singer_channel(i,
                                           is_active=True if i != 13 else False)
            song = create_song(i, singer,
                               is_active_image=True if i != 14 else False,
                               is_active_link=True if i != 15 else False)

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_singer_ok_test = self.client.get('/api/app/AllSinger/1', data={}, **header)
        get_singer_without_authorization = self.client.get('/api/app/AllSinger/1', data={})
        res = json.loads(str(get_singer_ok_test.content.decode("utf8")))

        assert (get_singer_ok_test.status_code == 200), str(get_singer_ok_test.content)
        assert (get_singer_without_authorization.status_code == 401), str(get_singer_without_authorization.content)

        assert (res['data']["single_song"].__len__() == 10), str(res['data']["single_song"])

        get_singer_ok_test = self.client.get('/api/app/AllSinger/2', data={}, **header)
        res = json.loads(str(get_singer_ok_test.content.decode("utf8")))

        assert (res['data']["single_song"].__len__() == 2), str(res['data']["single_song"])


class GetSingerChannelTest(TestCase):
    def test_get_singer_channel(self):
        # create a singer
        singer = create_singer_channel(1)

        # create a channel
        channel = create_singer_channel(2, True)

        # create songs and play list
        for i in range(4):
            song = create_song(i, singer,
                               is_active_link=True if i != 1 else False,
                               is_active_image=True if i != 2 else False)

            playlist = Playlists(
                playlist_id=i,
                name="test",
                cover="test",
                is_active=True,
            )
            playlist.save()
            playlist.songs.add(song)

        # create 12th podcaste
        podcast = list(map(lambda Id: create_song(Id + 1, channel, is_podcast=True), range(12, 24)))

        # create 5th Ads
        ads = list(map(lambda Id: create_ads(Id), range(5)))

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_singer_channel_ok_test = self.client.get('/api/app/singer_channel/1', data={}, **header)
        get_singer_channel_without_authorization = self.client.get('/api/app/singer_channel/1', data={})
        res = json.loads(str(get_singer_channel_ok_test.content.decode("utf8")))

        assert (get_singer_channel_ok_test.status_code == 200), str(get_singer_channel_ok_test.content)
        assert (get_singer_channel_without_authorization.status_code == 401), str(
            get_singer_channel_without_authorization.content)

        assert (res['data']["singer_channel"]["name"] == "test"), str(res['data']["singer_channel"]["name"])
        assert (res['data']["popular_songs"].__len__() == 2), str(res['data']["popular_songs"])
        assert (res['data']["playlist"].__len__() == 2), str(res['data']["playlist"])
        assert (res['data']["single_song"].__len__() == 2), str(res['data']["single_song"])
        assert (res['data']["ads"].__len__() == 3), str(res['data']["ads"])

        get_singer_channel_ok_test = self.client.get('/api/app/singer_channel/2', data={}, **header)
        res = json.loads(str(get_singer_channel_ok_test.content.decode("utf8")))
        assert (get_singer_channel_ok_test.status_code == 200), str(get_singer_channel_ok_test.content)
        assert (res['data']["popular_songs"].__len__() == 5), str(res['data']["popular_songs"])
        assert (res['data']["single_song"].__len__() == 5), str(res['data']["single_song"])

    def test_get_singer_channel_single_song(self):
        # create a singer
        singer = create_singer_channel(1)

        # create 12th songs
        song = list(map(lambda Id: create_song(Id + 1, singer), range(12)))

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_singer_channel_ok_test = self.client.get('/api/app/singer_channel/1/single_song_more/1', data={}, **header)
        get_singer_channel_without_authorization = self.client.get('/api/app/singer_channel/1/single_song_more/1',
                                                                   data={})
        res = json.loads(str(get_singer_channel_ok_test.content.decode("utf8")))

        assert (get_singer_channel_ok_test.status_code == 200), str(get_singer_channel_ok_test.content)
        assert (get_singer_channel_without_authorization.status_code == 401), str(
            get_singer_channel_without_authorization.content)

        assert (res['data']["page"] == 1), str(res['data']["page"])
        assert (res['data']["pages_count"] == 2), str(res['data']["pages_count"])
        assert (res['data']["single_song"].__len__() == 10), str(res['data']["single_song"])

        get_singer_channel_ok_test = self.client.get('/api/app/singer_channel/1/single_song_more/2', data={}, **header)
        res = json.loads(str(get_singer_channel_ok_test.content.decode("utf8")))

        assert (res['data']["page"] == 2), str(res['data']["page"])
        assert (res['data']["pages_count"] == 2), str(res['data']["pages_count"])
        assert (res['data']["single_song"].__len__() == 2), str(res['data']["single_song"])

    def test_get_singer_channel_popular_song(self):
        # create a singer
        singer = create_singer_channel(1)

        # create 12th songs
        song = list(map(lambda Id: create_song(Id + 1, singer), range(12)))

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_singer_channel_ok_test = self.client.get('/api/app/singer_channel/1/popular_song_more/1', data={}, **header)
        get_singer_channel_without_authorization = self.client.get('/api/app/singer_channel/1/popular_song_more/1',
                                                                   data={})
        res = json.loads(str(get_singer_channel_ok_test.content.decode("utf8")))

        assert (get_singer_channel_ok_test.status_code == 200), str(get_singer_channel_ok_test.content)
        assert (get_singer_channel_without_authorization.status_code == 401), str(
            get_singer_channel_without_authorization.content)

        assert (res['data']["page"] == 1), str(res['data']["page"])
        assert (res['data']["pages_count"] == 2), str(res['data']["pages_count"])
        assert (res['data']["single_song"].__len__() == 10), str(res['data']["single_song"])

        get_singer_channel_ok_test = self.client.get('/api/app/singer_channel/1/popular_song_more/2', data={}, **header)
        res = json.loads(str(get_singer_channel_ok_test.content.decode("utf8")))

        assert (res['data']["page"] == 2), str(res['data']["page"])
        assert (res['data']["pages_count"] == 2), str(res['data']["pages_count"])
        assert (res['data']["single_song"].__len__() == 2), str(res['data']["single_song"])


class GetPlayListTest(TestCase):
    def test_get_playlist(self):
        # create a singer
        singer = create_singer_channel(1)

        # create a channel
        channel = create_singer_channel(2, True)

        playlist = Playlists(
            playlist_id=1,
            name="test",
            cover="test",
            is_active=True,
        )
        playlist.save()

        # create songs and play list
        for i in range(7):
            song = create_song(i, singer)
            playlist.songs.add(song)

        # create 5th Ads
        ads = list(map(lambda Id: create_ads(Id), range(5)))

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_PlayList_ok_test = self.client.get('/api/app/PlayList/1', data={}, **header)
        get_PlayList_without_authorization = self.client.get('/api/app/PlayList/1', data={})
        res = json.loads(str(get_PlayList_ok_test.content.decode("utf8")))

        assert (get_PlayList_ok_test.status_code == 200), str(get_PlayList_ok_test.content)
        assert (get_PlayList_without_authorization.status_code == 401), str(get_PlayList_without_authorization.content)

        assert (res['data']["playlist_data"]["name"] == "test"), str(res['data']["playlist_data"]["name"])
        assert (res['data']["popular_song"].__len__() == 5), str(res['data']["popular_song"])
        assert (res['data']["playlist"].__len__() == 1), str(res['data']["playlist"])
        assert (res['data']["pages_count"] == 2), str(res['data']["pages_count"])
        assert (res['data']["single_song"].__len__() == 5), str(res['data']["single_song"])
        assert (res['data']["ads"].__len__() == 3), str(res['data']["ads"])

    def test_get_playlist_single_song(self):
        # create a singer
        singer = create_singer_channel(1)

        # create a channel
        channel = create_singer_channel(2, True)

        # create songs and play list
        playlist = Playlists(
            playlist_id=1,
            name="test",
            cover="test",
            is_active=True,
        )
        playlist.save()

        for i in range(4):
            song = create_song(i, singer,
                               is_active_link=True if i != 1 else False,
                               is_active_image=True if i != 2 else False)
            playlist.songs.add(song)

        # create play list
        playlist2 = Playlists(
            playlist_id=2,
            name="test2",
            cover="test2",
            is_active=True,
        )
        playlist2.save()

        # create 12th podcaste
        for i in range(4, 16):
            podcast = create_song(i, channel, is_podcast=True)
            playlist2.songs.add(podcast)

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_playlist_ok_test = self.client.get('/api/app/PlayList/1/single_song_more/1', data={}, **header)
        get_playlist_without_authorization = self.client.get('/api/app/PlayList/1/single_song_more/1', data={})
        res = json.loads(str(get_playlist_ok_test.content.decode("utf8")))

        assert (get_playlist_ok_test.status_code == 200), str(get_playlist_ok_test.content)
        assert (get_playlist_without_authorization.status_code == 401), str(get_playlist_without_authorization.content)

        assert (res['data']["page"] == 1), str(res['data']["page"])
        assert (res['data']["pages_count"] == 1), str(res['data']["pages_count"])
        assert (res['data']["data"].__len__() == 2), str(res['data']["data"].__len__())

        get_singer_channel_ok_test = self.client.get('/api/app/PlayList/2/single_song_more/3', data={}, **header)
        res = json.loads(str(get_singer_channel_ok_test.content.decode("utf8")))

        assert (res['data']["page"] == 3), str(res['data']["page"])
        assert (res['data']["pages_count"] == 3), str(res['data']["pages_count"])
        assert (res['data']["data"].__len__() == 2), str(res['data']["data"])

    def test_get_singer_channel_popular_song(self):
        # create a singer
        singer = create_singer_channel(1)

        # create a channel
        channel = create_singer_channel(2, True)

        # create songs and play list
        playlist = Playlists(
            playlist_id=1,
            name="test",
            cover="test",
            is_active=True,
        )
        playlist.save()

        for i in range(4):
            song = create_song(i, singer,
                               is_active_link=True if i != 1 else False,
                               is_active_image=True if i != 2 else False)
            playlist.songs.add(song)

        # create play list
        playlist2 = Playlists(
            playlist_id=2,
            name="test2",
            cover="test2",
            is_active=True,
        )
        playlist2.save()

        # create 12th podcaste
        for i in range(4, 16):
            podcast = create_song(i, channel, is_podcast=True)
            playlist2.songs.add(podcast)

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_PlayList_ok_test = self.client.get('/api/app/PlayList/1/popular_song_more/1', data={}, **header)
        get_PlayList_without_authorization = self.client.get('/api/app/PlayList/1/popular_song_more/1', data={})
        res = json.loads(str(get_PlayList_ok_test.content.decode("utf8")))

        assert (get_PlayList_ok_test.status_code == 200), str(get_PlayList_ok_test.content)
        assert (get_PlayList_without_authorization.status_code == 401), str(
            get_PlayList_without_authorization.content)

        assert (res['data']["page"] == 1), str(res['data']["page"])
        assert (res['data']["pages_count"] == 1), str(res['data']["pages_count"])
        assert (res['data']["data"].__len__() == 2), str(res['data']["data"].__len__())

        get_singer_channel_ok_test = self.client.get('/api/app/PlayList/2/popular_song_more/3', data={}, **header)
        res = json.loads(str(get_singer_channel_ok_test.content.decode("utf8")))

        assert (res['data']["page"] == 3), str(res['data']["page"])
        assert (res['data']["pages_count"] == 3), str(res['data']["pages_count"])
        assert (res['data']["data"].__len__() == 2), str(res['data']["data"])


class MoviesTest(TestCase):
    def test_Movies_view(self):
        # create a category
        create_Category(1)
        create_Category(2)

        # create 12th video
        video = list(map(lambda Id: create_video(Id + 1), range(12)))

        # # create 3th video
        for i in range(12, 16):
            video2 = create_video(i, category_id=2,
                                  is_active_image=True if i != 13 else False,
                                  is_active_link=True if i != 14 else False,
                                  )

        # create a slider video
        slider_video = SliderVideo(
            slider_id=1,
            video=video[0],
            image_link="test",
            is_show=True,
            is_childish=False,
            is_active=True,
        )
        slider_video.save()
        slider_video = SliderVideo(
            slider_id=2,
            video=video[1],
            image_link="test",
            is_show=True,
            is_childish=False,
            is_active=True,
        )
        slider_video.save()

        # create 5th Ads
        ads = list(map(lambda Id: create_ads(Id), range(5)))
        create_ads(6, is_video_ads=True, video=video[1])

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_home_ok_test = self.client.get('/api/app/Movies', data={}, **header)
        get_home_without_authorization = self.client.get('/api/app/Movies', data={})
        res = json.loads(str(get_home_ok_test.content.decode("utf8")))

        assert (get_home_ok_test.status_code == 200), str(get_home_ok_test.content)
        assert (get_home_without_authorization.status_code == 401), str(get_home_without_authorization.content)
        assert (res['data']["slider"].__len__() == 2), str(res['data']["slider"])
        assert (res['data']["category"]["category1"]["title"] == "test"), str(
            res['data']["category"]["category1"]["title"])
        assert (res['data']["newest_video"].__len__() == 10), str(res['data']["newest_video"])
        assert (res['data']["visited_videos"].__len__() == 10), str(res['data']["visited_videos"])
        assert (res['data']["category_data"]["category1"].__len__() == 10), str(
            res['data']["category_data"]["category1"])
        assert (res['data']["category_data"]["category2"].__len__() == 2), str(
            res['data']["category_data"])
        assert (res['data']["ads"].__len__() == 3), str(res['data']["ads"])
        assert (res['data']["banner"]["video_id"] == 2), str(res['data']["banner"]["video_id"])

        VideoCategory.objects.all().delete()

        get_home_ok_test = self.client.get('/api/app/Movies', data={}, **header)
        res = json.loads(str(get_home_ok_test.content.decode("utf8")))

        assert (res['data']["slider"].__len__() == 0), str(res['data']["slider"])
        assert (res['data']["category"] == {}), str(
            res['data']["category"])
        assert (res['data']["newest_video"].__len__() == 0), str(res['data']["newest_video"])
        assert (res['data']["visited_videos"].__len__() == 0), str(res['data']["visited_videos"])
        assert (res['data']["category_data"] == {}), str(
            res['data']["category_data"])

    def test_get_most_visited_videos(self):
        # create cat
        create_Category(1)

        for i in range(6):
            video = create_video(i,
                                 is_active_link=True if i != 1 else False,
                                 is_active_image=True if i != 2 else False,
                                 is_childish=True if i == 3 else False,
                                 view_count=10 if i == 4 else 9 if i == 0 else 2,
                                 )
        video = list(Util_App.get_most_visited_videos())
        assert (video.__len__() == 3), str(video)
        assert (video[0]["video_id"] == 4), str(video[0]["video_id"])
        assert (video[1]["video_id"] == 0), str(video[1]["video_id"])


class videoTest(TestCase):
    def test_video_view(self):
        create_Category(1)
        video = create_video(13)
        for i in range(12):
            VideoImages(
                image_id=i,
                video_id=13,
                is_active=True if i != 11 else False,
                name='test').save()
        for i in range(12):
            actor = VideoActors(
                actor_id=i,
                fa_name='test',
                en_name='test',
                avatar='test',
                is_active=True if i != 11 else False
            )
            actor.save()
            actor.videos.add(video)
        for i in range(1, 4):
            genre = VideoGenres(
                genre_id=i,
                name="test" + str(i),
            )
            genre.save()
            genre.videos.add(video)

        for i in range(12):
            video = create_video(i)
            for j in range(1, 4):
                genre = VideoGenres.objects.get(genre_id=j)
                genre.videos.add(video)

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_video_ok_test = self.client.get('/api/app/Video/13', data={}, **header)
        get_video_without_authorization = self.client.get('/api/app/Video/13', data={})
        res = json.loads(str(get_video_ok_test.content.decode("utf8")))

        assert (get_video_ok_test.status_code == 200), str(get_video_ok_test.content)
        assert (get_video_without_authorization.status_code == 401), str(get_video_without_authorization.content)
        assert (res['data']["suggested_videos"].__len__() == 10), str(res['data']["suggested_videos"])
        assert (res['data']["images"].__len__() == 11), str(res['data']["images"])
        assert (res['data']["actors"].__len__() == 11), str(res['data']["actors"])
        assert (res['data']["video_data"]["genres"].__len__() == 3), str(res['data']["video_data"]["genres"])

    def test_AllVideo_view(self):
        # create a category
        create_Category(1)

        # create 32th video
        for i in range(32):
            video = create_video(i,
                                 is_active_image=True if i % 13 else False,
                                 is_active_link=True if i % 14 else False,
                                 )

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_video_ok_test = self.client.get('/api/app/AllVideo/4', data={}, **header)
        get_video_without_authorization = self.client.get('/api/app/AllVideo/4', data={})
        res = json.loads(str(get_video_ok_test.content.decode("utf8")))

        assert (get_video_ok_test.status_code == 200), str(get_video_ok_test.content)
        assert (get_video_without_authorization.status_code == 401), str(get_video_without_authorization.content)

        assert (res['data']["page"] == 4), str(res['data']["page"])
        assert (res['data']["pages_count"] == 3), str(res['data']["pages_count"])
        assert (res['data']["videos"].__len__() == 7), str(res['data']["videos"])

    def test_videos_category_view(self):
        # create a category
        create_Category(2)

        # create 32th video
        for i in range(32):
            video = create_video(i, category_id=2,
                                 is_active_image=True if i % 13 else False,
                                 is_active_link=True if i % 14 else False,
                                 )

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_video_ok_test = self.client.get('/api/app/CatVideos/2/4', data={}, **header)
        get_video_without_authorization = self.client.get('/api/app/CatVideos/2/4', data={})
        res = json.loads(str(get_video_ok_test.content.decode("utf8")))

        assert (get_video_ok_test.status_code == 200), str(get_video_ok_test.content)
        assert (get_video_without_authorization.status_code == 401), str(get_video_without_authorization.content)

        assert (res['data']["name"] == "test"), str(res['data']["name"])
        assert (res['data']["page"] == 4), str(res['data']["page"])
        assert (res['data']["pages_count"] == 3), str(res['data']["pages_count"])
        assert (res['data']["cat_videos"].__len__() == 7), str(res['data']["cat_videos"])

    def test_videos_genre_view(self):
        # create a category
        create_Category(2)

        genre = VideoGenres(
            genre_id=2,
            name="test1",
        )
        genre.save()

        # create 32th video
        for i in range(32):
            video = create_video(i, category_id=2,
                                 is_active_image=True if i % 13 else False,
                                 is_active_link=True if i % 14 else False,
                                 )
            genre.videos.add(video)

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_video_ok_test = self.client.get('/api/app/GenreVideos/2/4', data={}, **header)
        get_video_without_authorization = self.client.get('/api/app/GenreVideos/2/4', data={})
        res = json.loads(str(get_video_ok_test.content.decode("utf8")))

        assert (get_video_ok_test.status_code == 200), str(get_video_ok_test.content)
        assert (get_video_without_authorization.status_code == 401), str(get_video_without_authorization.content)

        assert (res['data']["name"] == "test1"), str(res['data']["name"])
        assert (res['data']["page"] == 4), str(res['data']["page"])
        assert (res['data']["pages_count"] == 3), str(res['data']["pages_count"])
        assert (res['data']["genre_videos"].__len__() == 7), str(res['data']["genre_videos"])

    def test_videos_actor_view(self):
        # create a category
        create_Category(2)

        actor = VideoActors(
            actor_id=2,
            fa_name='test1',
            en_name='test2',
            avatar='test3',
            is_active=True
        )
        actor.save()

        # create 32th video
        for i in range(32):
            video = create_video(i, category_id=2,
                                 is_active_image=True if i % 13 else False,
                                 is_active_link=True if i % 14 else False,
                                 )
            actor.videos.add(video)

        header = {"HTTP_AUTHORIZATION": create_token()[1]}

        get_video_ok_test = self.client.get('/api/app/ActorVideos/2/4', data={}, **header)
        get_video_without_authorization = self.client.get('/api/app/ActorVideos/2/4', data={})
        res = json.loads(str(get_video_ok_test.content.decode("utf8")))

        assert (get_video_ok_test.status_code == 200), str(get_video_ok_test.content)
        assert (get_video_without_authorization.status_code == 401), str(get_video_without_authorization.content)

        assert (res['data']["name"] == "test1"), str(res['data']["name"])
        assert (res['data']["image"] == "test3"), str(res['data']["image"])
        assert (res['data']["page"] == 4), str(res['data']["page"])
        assert (res['data']["pages_count"] == 3), str(res['data']["pages_count"])
        assert (res['data']["actor_videos"].__len__() == 7), str(res['data']["actor_videos"])

import json
import os
import uuid
from datetime import datetime
from enum import Enum
from urllib.parse import urlparse

import requests

from apiApp.models import Songs, Singer_Channel, Album, Playlists, Ads
from apiApp.models import Videos, VideoCategory, VideoActors, VideoGenres, VideoImages
from apiWeb.models import SliderVideo, SliderSong, SliderHome, SliderAds

from variables import variables


class downloader_type(Enum):
    video_image = "0"
    video_link = "1"
    video_preview = "2"
    actor_image = "3"
    cat_image = "4"
    image_link = "5"
    slider_image = "6"
    song_image = "7"
    song_link = "8"
    singer_image = "9"
    playlist_cover = "10"
    album_image = "11"
    slider_song_image = "12"
    ads_image = "13"
    slider_ads_image = "14"


class Downloader:
    def __init__(self):
        self.image = variables().destination_image
        self.video = variables().destination_video
        self.song = variables().destination_song
        self.api = variables().api_downloader
        self.video_type = ["1", "2"]
        self.song_type = ["8"]
        self.image_type = ["0", "3", "4", "5", "6", "7", "9",
                           "10", "11", "12", "13", "14"]

    @staticmethod
    def url_name(url: str):
        # input => x.x.x.x/.../x.(png|jpg|mp4|mp3|mkv)
        # output=> x.(png|jpg|mp4|mp3|mkv)
        return os.path.basename(urlparse(url).path)

    @staticmethod
    def set_url(url: str):
        # input => x.x.x.x/x/...
        # output=> 192.168.255.252/x/...
        IP = variables().ip_box
        url = url.strip() if str(url).startswith('http://') else 'http://' + url.strip()
        return IP + urlparse(url).path

    @staticmethod
    def send_2_downloader(payload: list):
        headers = {
            'Content-Type': 'application/json'
        }
        payload = json.dumps(payload)
        print("downloader_data :", payload)
        response = requests.request("POST", Downloader().api, headers=headers, data=payload)
        f = open("log.txt", "a+")
        f.write("\r\n " + str(datetime.utcnow()) + " payload :" + payload + "\r\n")
        f.close()
        if response.status_code == 200:
            return True
        else:
            return False

    @staticmethod
    def downloader(url: str, type_model: str, type_id: str, Id: int = 0):
        try:
            # type_id => i = initial
            #         => u = update
            url = url.strip() if str(url).startswith('http://') else 'http://' + url.strip()
            is_exist = Downloader.exit_file(Downloader.url_name(url), type_model)[0]

            if is_exist:
                type = type_model + '/' + str(Id) + '.' + type_id
                Downloader.verify_download(url, type)
                return True
            else:
                type = type_model + '/' + str(Id) + '.' + type_id
                payload = {
                    "id": uuid.uuid4().hex,
                    "type": type,
                    "url": url
                }

                if type_model in Downloader().video_type:
                    payload["destination"] = Downloader().video
                elif type_model in Downloader().song_type:
                    payload["destination"] = Downloader().song
                else:
                    payload["destination"] = Downloader().image
                return payload
        except Exception as e:
            print("Error: ", str(e))
            return [str(e)]

    @staticmethod
    def remove_file(url_name: str, type: str):
        try:
            is_exist, path = Downloader.exit_file(url_name, type)
            if is_exist:
                os.remove(path)
                return True
            else:
                return False
        except Exception as e:
            print("Error_remove: ", str(e))
            return [str(e)]

    @staticmethod
    def exit_file(name_file: str, type_file: str):
        path = None
        if type_file in Downloader().video_type:
            path = Downloader().video
        elif type_file in Downloader().song_type:
            path = Downloader().song
        elif type_file in Downloader().image_type:
            path = Downloader().image
        path = path + '/' + name_file
        exists = os.path.exists(path)
        if exists:
            return True, path
        else:
            return False, False

    @staticmethod
    def verify_download(url: str, type: str):
        type_download = type.split('.')[1]
        type_model = type.split('.')[0].split('/')[0]
        type_id = type.split('.')[0].split('/')[1]
        # initial download
        if type_download == 'i':
            # video image
            Videos.objects.filter(video_id=type_id).update(is_active_image=True) \
                if downloader_type.video_image.value == type_model else None
            # video link
            Videos.objects.filter(video_id=type_id).update(is_active_link=True) \
                if downloader_type.video_link.value == type_model else None
            # video preview
            Videos.objects.filter(video_id=type_id).update(is_active_preview=True) \
                if downloader_type.video_preview.value == type_model else None
            # actor image
            VideoActors.objects.filter(actor_id=type_id).update(is_active=True) \
                if downloader_type.actor_image.value == type_model else None
            # category image
            VideoCategory.objects.filter(category_id=type_id).update(is_active=True) \
                if downloader_type.cat_image.value == type_model else None
            # image link
            VideoImages.objects.filter(image_id=type_id).update(is_active=True) \
                if downloader_type.image_link.value == type_model else None
            # slider video image
            SliderVideo.objects.filter(slider_id=type_id).update(is_active=True) \
                if downloader_type.slider_image.value == type_model else None
            # Singer Or Channel image
            Singer_Channel.objects.filter(singer_id=type_id).update(is_active=True) \
                if downloader_type.singer_image.value == type_model else None
            # song link
            Songs.objects.filter(song_id=type_id).update(is_active_link=True) \
                if downloader_type.song_link.value == type_model else None
            # song image
            Songs.objects.filter(song_id=type_id).update(is_active_image=True) \
                if downloader_type.song_image.value == type_model else None
            # album
            Album.objects.filter(album_id=type_id).update(is_active=True) \
                if downloader_type.album_image.value == type_model else None
            # playlist
            Playlists.objects.filter(playlist_id=type_id).update(is_active=True) \
                if downloader_type.playlist_cover.value == type_model else None
            # slider song image
            SliderSong.objects.filter(slider_id=type_id).update(is_active=True) \
                if downloader_type.slider_song_image.value == type_model else None
            # slider ads image
            SliderAds.objects.filter(slider_id=type_id).update(is_active=True) \
                if downloader_type.slider_ads_image.value == type_model else None
            # ads image
            Ads.objects.filter(ad_id=type_id).update(is_active=True) \
                if downloader_type.ads_image.value == type_model else None

        # update download
        else:
            # video image
            if downloader_type.video_image.value == type_model:
                video = Videos.objects.get(video_id=type_id)
                Downloader.remove_file(Downloader.url_name(video.image_link), downloader_type.video_image.value)
                video.image_link = Downloader.set_url(url)
                video.is_active_image = True
                video.save()
            # video link
            if downloader_type.video_link.value == type_model:
                video = Videos.objects.get(video_id=type_id)
                Downloader.remove_file(Downloader.url_name(video.link), downloader_type.video_link.value)
                video.link = Downloader.set_url(url)
                video.is_active_link = True
                video.save()
            # video preview
            if downloader_type.video_preview.value == type_model:
                video = Videos.objects.get(video_id=type_id)
                Downloader.remove_file(Downloader.url_name(video.preview_link), downloader_type.video_preview.value)
                video.preview_link = Downloader.set_url(url)
                video.is_active_preview = True
                video.save()
            # actor image
            if downloader_type.actor_image.value == type_model:
                actor = VideoActors.objects.get(actor_id=type_id)
                Downloader.remove_file(Downloader.url_name(actor.avatar), downloader_type.actor_image.value)
                actor.avatar = Downloader.set_url(url)
                actor.is_active = True
                actor.save()

            # category image
            if downloader_type.cat_image.value == type_model:
                category = VideoCategory.objects.get(category_id=type_id)
                Downloader.remove_file(Downloader.url_name(category.image_link), downloader_type.cat_image.value)
                category.image_link = Downloader.set_url(url)
                category.is_active = True
                category.save()

            # image link
            if downloader_type.image_link.value == type_model:
                image = VideoImages.objects.get(image_id=type_id)
                Downloader.remove_file(Downloader.url_name(image.link), downloader_type.image_link.value)
                image.link = Downloader.set_url(url)
                image.is_active = True
                image.save()

            # slider image
            if downloader_type.slider_image.value == type_model:
                slider = SliderVideo.objects.get(slider_id=type_id)
                Downloader.remove_file(Downloader.url_name(slider.image_link), downloader_type.slider_image.value)
                slider.image_link = Downloader.set_url(url)
                slider.is_active = True
                slider.save()

            # singer or channel
            if downloader_type.singer_image.value == type_model:
                singer = Singer_Channel.objects.get(singer_id=type_id)
                Downloader.remove_file(Downloader.url_name(singer.image_link), downloader_type.singer_image.value)
                singer.image_link = Downloader.set_url(url)
                singer.is_active = True
                singer.save()

            # song link
            if downloader_type.song_link.value == type_model:
                song = Songs.objects.get(song_id=type_id)
                Downloader.remove_file(Downloader.url_name(song.link), downloader_type.song_link.value)
                song.link = Downloader.set_url(url)
                song.is_active_link = True
                song.save()

            # song image
            if downloader_type.song_image.value == type_model:
                song = Songs.objects.get(song_id=type_id)
                Downloader.remove_file(Downloader.url_name(song.image_link), downloader_type.song_image.value)
                song.image_link = Downloader.set_url(url)
                song.is_active_image = True
                song.save()

            # Album image
            if downloader_type.album_image.value == type_model:
                album = Album.objects.get(album_id=type_id)
                Downloader.remove_file(Downloader.url_name(album.image_link), downloader_type.album_image.value)
                album.image_link = Downloader.set_url(url)
                album.is_active = True
                album.save()

            # Playlists image
            if downloader_type.playlist_cover.value == type_model:
                playlists = Playlists.objects.get(playlist_id=type_id)
                Downloader.remove_file(Downloader.url_name(playlists.cover), downloader_type.playlist_cover.value)
                playlists.cover = Downloader.set_url(url)
                playlists.is_active = True
                playlists.save()

            # SliderSong image
            if downloader_type.slider_song_image.value == type_model:
                sliderSong = SliderSong.objects.get(slider_id=type_id)
                Downloader.remove_file(Downloader.url_name(sliderSong.image_link),
                                       downloader_type.slider_song_image.value)
                sliderSong.image_link = Downloader.set_url(url)
                sliderSong.is_active = True
                sliderSong.save()

            # SliderAds image
            if downloader_type.slider_ads_image.value == type_model:
                sliderAds = SliderAds.objects.get(slider_id=type_id)
                Downloader.remove_file(Downloader.url_name(sliderAds.image_url), downloader_type.slider_ads_image.value)
                sliderAds.image_url = Downloader.set_url(url)
                sliderAds.is_active = True
                sliderAds.save()

            # Ads image
            if downloader_type.ads_image.value == type_model:
                ads = Ads.objects.get(ad_id=type_id)
                Downloader.remove_file(Downloader.url_name(ads.image_url), downloader_type.ads_image.value)
                ads.image_url = Downloader.set_url(url)
                ads.is_active = True
                ads.save()

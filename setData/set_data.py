import os
import json
from datetime import datetime
from enum import Enum
from urllib.parse import urlparse

from apiApp.models import Songs, Singer_Channel, Album, Playlists, Ads
from apiApp.models import Videos, VideoCategory, VideoActors, VideoGenres, VideoImages
from apiWeb.models import SliderVideo, SliderSong, SliderHome, SliderAds
from setData.downloader import Downloader

from apiApp.models import VideoImages

from apiApp.models import VideoCategory


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


class SetData:
    @staticmethod
    def set_video(data_videos: list):
        try:
            video_id = set()
            download_data = []
            if data_videos:
                for data_video in data_videos:
                    # set or update video
                    video_id.add(data_video['video_id'])
                    cat = SetData.add_cat(data_video["category"])
                    video = SetData.add_video(data_video, cat[0])
                    actor = SetData.add_actor(data_video["actors"], video[0])
                    genre = SetData.add_genre(data_video["genres"], video[0])
                    image = SetData.add_image(data_video["image"], video[0])
                    slider = SetData.add_slider_video(data_video["slider"], video[0])
                    download_data.extend(cat[1]) if cat[1] else None
                    download_data.extend(video[1]) if video[1] else None
                    download_data.extend(actor) if actor else None
                    download_data.extend(image) if image else None
                    download_data.extend(slider) if slider else None

            # Delete Video
            video_exist = Videos.objects.all()
            exists_id = set(Id for Id in video_exist.values_list('video_id', flat=True))
            dels_id = exists_id - video_id
            for video_id in dels_id:
                video = video_exist.get(video_id=video_id)
                remove_image = Downloader.remove_file(Downloader.url_name(video.image_link),
                                                      downloader_type.video_image.value)
                remove_link = Downloader.remove_file(Downloader.url_name(video.link),
                                                     downloader_type.video_link.value)
                remove_preview = Downloader.remove_file(Downloader.url_name(video.preview_link),
                                                        downloader_type.video_preview.value) \
                    if video.preview_link else None
                # delete image
                images = VideoImages.objects.filter(video=video)
                if images:
                    for image in images:
                        remove = Downloader.remove_file(Downloader.url_name(image.link),
                                                        downloader_type.image_link.value)
                        image.delete() if remove else None
                # delete slider
                sliders = SliderVideo.objects.filter(video=video)
                if sliders:
                    for slider in sliders:
                        remove = Downloader.remove_file(Downloader.url_name(slider.image_link),
                                                        downloader_type.slider_image.value)
                        slider.delete() if remove else None
                # delete ads
                ads = Ads.objects.filter(video=video)
                if ads:
                    for ad in ads:
                        remove = Downloader.remove_file(Downloader.url_name(ad.image_url),
                                                        downloader_type.ads_image.value)
                        ad.delete() if remove else None
                video.delete()
            return download_data
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set all video :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def add_video(data_video: dict, cat: VideoCategory):
        try:
            if data_video:
                video = Videos.objects.filter(video_id=data_video['video_id'])
                if not video:
                    # set video
                    new_video = Videos()
                    new_video.video_id = data_video['video_id']
                    new_video.fa_name = data_video['fa_name']
                    new_video.en_name = data_video['en_name']
                    new_video.slug = data_video['slug']
                    new_video.image_link = Downloader.set_url(data_video['image_link'])
                    new_video.view_count = data_video['view_count']
                    new_video.min_age = data_video['min_age']
                    new_video.description = data_video['description']
                    new_video.length = data_video['length']
                    new_video.summary = data_video['summary']
                    new_video.imdb_rating = data_video['imdb_rating']
                    new_video.director = data_video['director']
                    new_video.country_product = data_video['country_product']
                    new_video.is_dubbed = data_video['is_dubbed']
                    new_video.is_childish = data_video['is_childish']
                    new_video.link = Downloader.set_url(data_video['link'])
                    new_video.preview_link = Downloader.set_url(data_video['preview_link']) \
                        if data_video['preview_link'] else None
                    new_video.added_at = data_video['added_at']
                    new_video.category = cat
                    new_video.save()
                    # downloader
                    payload = [Downloader.downloader(data_video['image_link'], downloader_type.video_image.value, 'i',
                                                     new_video.video_id),
                               Downloader.downloader(data_video['link'], downloader_type.video_link.value, 'i',
                                                     new_video.video_id)]
                    payload.append(
                        Downloader.downloader(data_video['preview_link'], downloader_type.video_preview.value, 'i',
                                              new_video.video_id)) if data_video['preview_link'] else None
                    return new_video, payload
                else:
                    # update
                    one_video = video.first()
                    video.update(video_id=data_video["video_id"]) if one_video.video_id != \
                                                                     data_video["video_id"] else None
                    video.update(fa_name=data_video["fa_name"]) if one_video.fa_name != \
                                                                   data_video["fa_name"] else None
                    video.update(en_name=data_video["en_name"]) if one_video.en_name != \
                                                                   data_video["en_name"] else None
                    video.update(slug=data_video["slug"]) if one_video.slug != \
                                                             data_video["slug"] else None
                    video.update(view_count=data_video["view_count"]) if one_video.view_count != \
                                                                         data_video["view_count"] else None
                    video.update(min_age=data_video["min_age"]) if one_video.min_age != \
                                                                   data_video["min_age"] else None
                    video.update(description=data_video["description"]) if one_video.description != \
                                                                           data_video["description"] else None
                    video.update(length=data_video["length"]) if one_video.length != \
                                                                 data_video["length"] else None
                    video.update(summary=data_video["summary"]) if one_video.summary != \
                                                                   data_video["summary"] else None
                    video.update(imdb_rating=data_video["imdb_rating"]) if one_video.imdb_rating != \
                                                                           data_video["imdb_rating"] else None
                    video.update(director=data_video["director"]) if one_video.director != \
                                                                     data_video["director"] else None
                    video.update(country_product=data_video["country_product"]) if one_video.country_product != \
                                                                                   data_video[
                                                                                       "country_product"] else None
                    video.update(is_dubbed=data_video["is_dubbed"]) if one_video.is_dubbed != \
                                                                       data_video["is_dubbed"] else None

                    video.update(is_childish=data_video["is_childish"]) if one_video.is_childish != \
                                                                           data_video["is_childish"] else None
                    video.update(added_at=data_video["added_at"]) if one_video.added_at != \
                                                                     data_video["added_at"] else None
                    video.update(category=cat) if one_video.category != cat else None
                    payload = []
                    new_image = Downloader.url_name(data_video['image_link'])
                    old_image = Downloader.url_name(one_video.image_link)
                    payload.append(Downloader.downloader(data_video['image_link'], downloader_type.video_image.value,
                                                         'u', one_video.video_id)) if old_image != new_image else None

                    new_link = Downloader.url_name(data_video['link'])
                    old_link = Downloader.url_name(one_video.link)
                    payload.append(Downloader.downloader(data_video['link'], downloader_type.video_link.value, 'u',
                                                         one_video.video_id)) if old_link != new_link else None
                    if data_video['preview_link']:
                        new_preview = Downloader.url_name(data_video['preview_link'])
                        old_preview = Downloader.url_name(one_video.preview_link)
                        payload.append(Downloader.downloader(data_video['preview_link'],
                                                             downloader_type.video_preview.value, 'u',
                                                             one_video.video_id)) \
                            if old_preview != new_preview else None
                    else:
                        if one_video.preview_link:
                            Downloader.remove_file(Downloader.url_name(one_video.preview_link),
                                                   downloader_type.video_preview.value)
                        video.update(preview_link=data_video['preview_link'])
                    return one_video, payload
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set one video :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def add_cat(cat_data: dict):
        try:
            payload = []
            if cat_data:
                cat = VideoCategory.objects.filter(category_id=cat_data['category_id'])
                if cat:
                    if cat_data["update"]:
                        # update
                        one_cat = cat.first()
                        cat.update(title=cat_data["title"]) if one_cat.title != cat_data["title"] else None
                        new_image = Downloader.url_name(cat_data['image_link'])
                        old_image = Downloader.url_name(one_cat.image_link)
                        payload.append(Downloader.downloader(cat_data['image_link'], downloader_type.cat_image.value,
                                                             'u', one_cat.category_id)) \
                            if old_image != new_image else None
                    return cat.first(), payload
                else:
                    # set cat
                    new_cat = VideoCategory()
                    new_cat.category_id = cat_data['category_id']
                    new_cat.image_link = Downloader.set_url(cat_data['image_link'])
                    new_cat.title = cat_data['title']
                    new_cat.save()
                    # download
                    payload.append(Downloader.downloader(cat_data['image_link'], downloader_type.cat_image.value, 'i',
                                                         new_cat.category_id))
                    return new_cat, payload
        except Exception as e:
            return [str(e)]

    @staticmethod
    def add_actor(actor_datas: list, video: Videos):
        try:
            actor_id = set()
            payload = []
            if actor_datas:
                for actor_data in actor_datas:
                    actor_id.add(actor_data['actor_id'])
                    actor = VideoActors.objects.filter(actor_id=actor_data['actor_id'])
                    if actor:
                        # update
                        one_actor = actor.first()
                        is_actor = video.videoactors_set.filter(actor_id=actor_data['actor_id']).first()
                        if not is_actor:
                            one_actor.videos.add(video)
                        if actor_data['update']:
                            actor.update(fa_name=actor_data["fa_name"]) if one_actor.fa_name != \
                                                                           actor_data["fa_name"] else None
                            actor.update(en_name=actor_data["en_name"]) if one_actor.en_name != \
                                                                           actor_data["en_name"] else None
                            actor.update(description=actor_data["description"]) if one_actor.description != \
                                                                                   actor_data["description"] else None
                            new_image = Downloader.url_name(actor_data['avatar'])
                            old_image = Downloader.url_name(one_actor.avatar)
                            payload.append(Downloader.downloader(actor_data['avatar'], downloader_type.actor_image.value
                                                                 , 'u', one_actor.actor_id)) \
                                if old_image != new_image else None
                    else:
                        # set actor
                        new_actor = VideoActors()
                        new_actor.actor_id = actor_data['actor_id']
                        new_actor.fa_name = actor_data['fa_name']
                        new_actor.en_name = actor_data['en_name']
                        new_actor.description = actor_data['description']
                        new_actor.avatar = Downloader.set_url(actor_data['avatar'])
                        new_actor.save()
                        new_actor.videos.add(video)
                        # download
                        payload.append(Downloader.downloader(actor_data['avatar'], downloader_type.actor_image.value,
                                                             'i', new_actor.actor_id))
            # delete
            actor_exists = VideoActors.objects.filter(videos=video)
            exists_id = set(Id[0] for Id in actor_exists.values_list('actor_id'))
            dels_id = exists_id - actor_id
            for exist_id in dels_id:
                actor = actor_exists.get(actor_id=exist_id)
                video.videoactors_set.remove(actor)
            return payload
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set actor :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def add_genre(genre_datas: list, video: Videos):
        try:
            genre_id = set()
            if genre_datas:
                for genre_data in genre_datas:
                    genre_id.add(genre_data['genre_id'])
                    genre = VideoGenres.objects.filter(genre_id=genre_data['genre_id']).first()
                    if genre:
                        # update
                        is_genre = video.videogenres_set.filter(genre_id=genre_data['genre_id']).first()
                        if not is_genre:
                            genre.videos.add(video)
                        if genre.name != genre_data['name']:
                            genre.name = genre_data['name']
                            genre.save()
                    else:
                        # Set Genre
                        new_genre = VideoGenres()
                        new_genre.genre_id = genre_data['genre_id']
                        new_genre.name = genre_data['name']
                        new_genre.save()
                        new_genre.videos.add(video)
            # remove video
            genre_exists = VideoGenres.objects.filter(videos=video)
            id_exists = set(Id[0] for Id in genre_exists.values_list('genre_id'))
            dels_id = id_exists - genre_id
            for genre_id in dels_id:
                genre = genre_exists.get(genre_id=genre_id)
                video.videogenres_set.remove(genre)
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set genre :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def add_image(image_datas: dict, video: Videos):
        try:
            payload = []
            images_id = set()
            if image_datas:
                for image_data in image_datas:
                    images_id.add(image_data['image_id'])
                    image = VideoImages.objects.filter(image_id=image_data['image_id'])
                    if not image:
                        # Set Image
                        new_image = VideoImages()
                        new_image.image_id = image_data['image_id']
                        new_image.link = Downloader.set_url(image_data['link'])
                        new_image.is_sticker = image_data['is_sticker']
                        new_image.name = image_data['name']
                        new_image.video = video
                        new_image.save()
                        # download
                        payload.append(Downloader.downloader(image_data['link'], downloader_type.image_link.value, 'i',
                                                             new_image.image_id))
                    else:
                        # update
                        one_image = image.first()
                        image.update(is_sticker=image_data["is_sticker"]) if one_image.is_sticker != \
                                                                             image_data["is_sticker"] else None
                        image.update(name=image_data["name"]) if one_image.name != \
                                                                 image_data["name"] else None
                        new_image = Downloader.url_name(image_data['link'])
                        old_image = Downloader.url_name(one_image.link)
                        payload.append(Downloader.downloader(image_data['link'], downloader_type.image_link.value, 'u',
                                                             one_image.image_id)) if old_image != new_image else None
            # delete
            image_exists = VideoImages.objects.filter(video=video)
            exists_id = set(Id[0] for Id in image_exists.values_list('image_id'))
            dels = exists_id - images_id
            for exist_id in dels:
                image = image_exists.get(image_id=exist_id)
                remove = Downloader.remove_file(Downloader.url_name(image.link), downloader_type.image_link.value)
                image.delete() if remove else None
            return payload
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set image :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def add_slider_video(slider_datas: list, video: Videos):
        try:
            slider_id = set()
            payload = []
            if slider_datas:
                for slider_data in slider_datas:
                    slider_id.add(slider_data['slider_id'])
                    slider = SliderVideo.objects.filter(slider_id=slider_data['slider_id'])
                    if not slider:
                        # Set Video
                        new_slider = SliderVideo()
                        new_slider.slider_id = slider_data['slider_id']
                        new_slider.image_link = Downloader.set_url(slider_data['image_link'])
                        new_slider.is_show = slider_data['is_show']
                        new_slider.is_childish = slider_data['is_childish']
                        new_slider.video = video
                        new_slider.save()
                        # download
                        payload.append(
                            Downloader.downloader(slider_data['image_link'], downloader_type.slider_image.value,
                                                  'i', new_slider.slider_id))
                    else:
                        # update
                        slider_one = slider.first()
                        new_image = Downloader.url_name(slider_data['image_link'])
                        old_image = Downloader.url_name(slider_one.image_link)
                        payload.append(
                            Downloader.downloader(slider_data['image_link'], downloader_type.slider_image.value,
                                                  'u', slider_one.slider_id)) if old_image != new_image else None

                        slider.update(is_show=slider_data['is_show']) if \
                            slider_one.is_show != slider_data['is_show'] else None
                        slider.update(is_childish=slider_data['is_childish']) if \
                            slider_one.is_childish != slider_data['is_childish'] else None
                        slider.update(video=video) if slider_one.video != video else None
            # delete
            slider_exists = SliderVideo.objects.filter(video=video)
            id_exist = set(Id[0] for Id in slider_exists.values_list('slider_id'))
            del_id = id_exist - slider_id
            for slider_id in del_id:
                slider = slider_exists.get(slider_id=slider_id)
                remove = Downloader.remove_file(Downloader.url_name(slider.image_link),
                                                downloader_type.slider_song_image.value)
                slider.delete() if remove else None
            return payload
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set slider video :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    # ===========================================song===================================================================
    @staticmethod
    def set_song(data_songs: list):
        try:
            singer_id = set()
            album_id = set()
            song_id = set()
            download_data = []
            if data_songs:
                for data_song in data_songs:
                    # set song data
                    singer_id.add(data_song["singer"]['singer_id']) if data_song["singer"] else None
                    album_id.add(data_song["album"]['album_id']) if data_song["album"] else None
                    song_id.add(data_song["song_id"])
                    singer = SetData.add_singer(data_song['singer'])
                    album = SetData.add_album(data_song['album'])
                    song = SetData.add_song(data_song, singer[0], album[0])
                    playlist = SetData.add_playlist(data_song['play_list'], song[0])
                    slider = SetData.add_slider_song(data_song['slider'], song[0])
                    download_data.append(singer[1]) if singer[1] else None
                    download_data.append(album[1]) if album[1] else None
                    download_data.extend(song[1]) if song[1] else None
                    download_data.extend(playlist) if playlist else None
                    download_data.extend(slider) if slider else None

            # delete song
            song_exist = Songs.objects.all()
            id_exist = set(Id[0] for Id in song_exist.values_list('song_id'))
            del_id = id_exist - song_id
            for song_id in del_id:
                song = song_exist.get(song_id=song_id)
                slider_exists = SliderSong.objects.filter(Song=song)
                exists_id = set(Id[0] for Id in slider_exists.values_list('slider_id'))
                for slider_id in exists_id:
                    slider = slider_exists.get(slider_id=slider_id)
                    remove = Downloader.remove_file(Downloader.url_name(slider.image_link),
                                                    downloader_type.slider_song_image.value)
                    slider.delete() if remove else None

                remove = Downloader.remove_file(Downloader.url_name(song.image_link), downloader_type.song_image.value)
                remove = Downloader.remove_file(Downloader.url_name(song.link),
                                                downloader_type.song_link.value) if remove \
                    else None

                song.delete()  # if remove else None

            # delete singer
            singer_exist = Singer_Channel.objects.all()
            id_exist = set(Id[0] for Id in singer_exist.values_list('singer_id'))
            del_id = id_exist - singer_id
            for singer_id in del_id:
                singer = singer_exist.get(singer_id=singer_id)
                remove = Downloader.remove_file(Downloader.url_name(singer.image_link),
                                                downloader_type.singer_image.value)
                singer.delete()  # if remove else None

            # delete album
            album_exist = Album.objects.all()
            id_exist = set(Id[0] for Id in album_exist.values_list('album_id'))
            del_id = id_exist - album_id
            for album_id in del_id:
                album = album_exist.get(album_id=album_id)
                remove = Downloader.remove_file(Downloader.url_name(album.image_link),
                                                downloader_type.album_image.value)
                album.delete()  # if remove else None

            return download_data
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set all song :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def add_song(song_data: dict, singer: Singer_Channel, album: Album):
        try:
            if song_data:
                song = Songs.objects.filter(song_id=song_data['song_id'])
                if not song:
                    # set song
                    new_song = Songs()
                    new_song.song_id = song_data['song_id']
                    new_song.fa_name = song_data['fa_name']
                    new_song.en_name = song_data['en_name']
                    new_song.image_link = Downloader.set_url(song_data['image_link'])
                    new_song.view_count = song_data['view_count']
                    new_song.min_age = song_data['min_age']
                    new_song.description = song_data['description']
                    new_song.singer = singer
                    new_song.album = album
                    new_song.length = song_data['length']
                    new_song.link = Downloader.set_url(song_data['link'])
                    new_song.added_at = song_data['added_at']
                    new_song.is_podcast = song_data['is_podcast']
                    new_song.is_childish = song_data['is_childish']
                    new_song.save()
                    # downloader
                    payload = [Downloader.downloader(song_data['image_link'], downloader_type.song_image.value, 'i',
                                                     new_song.song_id),
                               Downloader.downloader(song_data['link'], downloader_type.song_link.value, 'i',
                                                     new_song.song_id)]
                    return new_song, payload
                else:
                    # update
                    one_song = song.first()
                    song.update(song_id=song_data["song_id"]) if one_song.song_id != song_data["song_id"] \
                        else None
                    song.update(fa_name=song_data["fa_name"]) if one_song.fa_name != song_data["fa_name"] \
                        else None
                    song.update(en_name=song_data["en_name"]) if one_song.en_name != song_data["en_name"] \
                        else None
                    song.update(view_count=song_data["view_count"]) if one_song.view_count != song_data["view_count"] \
                        else None
                    song.update(min_age=song_data["min_age"]) if one_song.min_age != song_data["min_age"] \
                        else None
                    song.update(description=song_data["description"]) if one_song.description != song_data[
                        "description"] \
                        else None
                    song.update(singer=singer) if one_song.singer != singer \
                        else None
                    song.update(album=album) if one_song.album != album \
                        else None
                    song.update(length=song_data["length"]) if one_song.length != song_data["length"] \
                        else None
                    song.update(added_at=song_data["added_at"]) if one_song.added_at != song_data["added_at"] \
                        else None
                    song.update(is_podcast=song_data["is_podcast"]) if one_song.is_podcast != song_data["is_podcast"] \
                        else None
                    song.update(is_childish=song_data["is_childish"]) if one_song.is_childish != song_data[
                        "is_childish"] \
                        else None
                    payload = []
                    new_image = Downloader.url_name(song_data['image_link'])
                    old_image = Downloader.url_name(one_song.image_link)
                    if old_image != new_image:
                        payload.append(
                            Downloader.downloader(song_data['image_link'], downloader_type.song_image.value, 'u',
                                                  one_song.song_id))

                    new_image = Downloader.url_name(song_data["link"])
                    old_image = Downloader.url_name(one_song.link)
                    if old_image != new_image:
                        payload.append(Downloader.downloader(song_data["link"], downloader_type.song_link.value, 'u',
                                                             one_song.song_id))
                    return one_song, payload
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set one song :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def add_singer(singer_data: dict):
        try:
            payload = {}
            if singer_data:
                singer = Singer_Channel.objects.filter(singer_id=singer_data['singer_id'])
                if not singer:
                    # set singer
                    new_singer = Singer_Channel()
                    new_singer.singer_id = singer_data['singer_id']
                    new_singer.fa_name = singer_data['fa_name']
                    new_singer.en_name = singer_data['en_name']
                    new_singer.image_link = Downloader.set_url(singer_data['image_link'])
                    new_singer.is_channel = singer_data['is_channel']
                    new_singer.save()
                    # download
                    payload = Downloader.downloader(singer_data['image_link'], downloader_type.singer_image.value, 'i',
                                                    new_singer.singer_id)
                    return new_singer, payload
                else:
                    # update
                    one_singer = singer.first()
                    if singer_data["update"]:
                        singer.update(fa_name=singer_data["fa_name"]) if one_singer.fa_name != \
                                                                         singer_data["fa_name"] else None
                        singer.update(en_name=singer_data["en_name"]) if one_singer.en_name != \
                                                                         singer_data["en_name"] else None
                        singer.update(is_channel=singer_data["is_channel"]) if one_singer.is_channel != \
                                                                               singer_data["is_channel"] else None

                        new_image = Downloader.url_name(singer_data['image_link'])
                        old_image = Downloader.url_name(one_singer.image_link)
                        if old_image != new_image:
                            payload = Downloader.downloader(singer_data['image_link'],
                                                            downloader_type.singer_image.value, 'u',
                                                            one_singer.singer_id)
                    return singer.first(), payload
            else:
                return None, payload
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set singer :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def add_album(album_data: dict):
        try:
            payload = {}
            if album_data:
                album = Album.objects.filter(album_id=album_data['album_id'])
                if not album:
                    # set album
                    new_album = Album()
                    new_album.album_id = album_data['album_id']
                    new_album.name = album_data['name']
                    new_album.image_link = Downloader.set_url(album_data['image_link'])
                    new_album.save()
                    payload = Downloader.downloader(album_data['image_link'], downloader_type.album_image.value, 'i',
                                                    new_album.album_id)
                    return new_album, payload
                else:
                    # update
                    one_album = album.first()
                    if album_data['update']:
                        album.update(name=album_data['name']) if one_album.name != album_data else None

                        new_image = Downloader.url_name(album_data['image_link'])
                        old_image = Downloader.url_name(one_album.image_link)
                        if old_image != new_image:
                            payload = Downloader.downloader(album_data['image_link'], downloader_type.album_image.value,
                                                            'u', one_album.album_id)
                    return one_album, payload
            return None, payload
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set album :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def add_playlist(playlist_datas: list, song: Songs):
        try:
            playlist_id = set()
            payload = []
            if playlist_datas:
                for playlist_data in playlist_datas:
                    playlist_id.add(playlist_data['playlist_id'])
                    playlist = Playlists.objects.filter(playlist_id=playlist_data['playlist_id'])
                    if playlist:
                        # update
                        one_playlist = playlist.first()
                        is_playlist = song.playlists_set.filter(playlist_id=playlist_data['playlist_id']).first()
                        if not is_playlist:
                            one_playlist.songs.add(song)
                        if playlist_data["update"]:
                            playlist.update(name=playlist_data['name']) if one_playlist.name != playlist_data['name'] \
                                else None
                            playlist.update(sort_by=playlist_data['sort_by']) if one_playlist.sort_by != playlist_data[
                                'sort_by'] else None
                            new_cover = Downloader.url_name(playlist_data['cover'])
                            old_cover = Downloader.url_name(one_playlist.cover)
                            if old_cover != new_cover:
                                payload.append(Downloader.downloader(playlist_data['cover'],
                                                                     downloader_type.playlist_cover.value, 'u',
                                                                     one_playlist.playlist_id))
                    else:
                        # set
                        new_playlist = Playlists()
                        new_playlist.playlist_id = playlist_data['playlist_id']
                        new_playlist.name = playlist_data['name']
                        new_playlist.cover = Downloader.set_url(playlist_data['cover'])
                        new_playlist.sort_by = Downloader.set_url(playlist_data['sort_by'])
                        new_playlist.save()
                        new_playlist.songs.add(song)
                        payload.append(Downloader.downloader(playlist_data['cover'],
                                                             downloader_type.playlist_cover.value,
                                                             'i', new_playlist.playlist_id))
            # delete relationships
            playlist_exist = Playlists.objects.filter(songs=song)
            id_exist = set(Id[0] for Id in playlist_exist.values_list('playlist_id'))
            del_id = id_exist - playlist_id
            [song.playlists_set.remove(playlist_exist.filter(playlist_id=playlist_id).first()) for playlist_id in
             del_id]
            return payload
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set playlist :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def add_slider_song(slider_datas: list, song: Songs):
        try:
            slider_id = set()
            payload = []
            if slider_datas:
                for slider_data in slider_datas:
                    slider_id.add(slider_data['slider_id'])
                    slider = SliderSong.objects.filter(slider_id=slider_data['slider_id'])
                    if not slider:
                        # set slider
                        new_slider = SliderSong()
                        new_slider.slider_id = slider_data['slider_id']
                        new_slider.image_link = Downloader.set_url(slider_data['image_link'])
                        new_slider.lyric = slider_data['lyric']
                        new_slider.release_date = slider_data['release_date']
                        new_slider.tarane = slider_data['tarane']
                        new_slider.tuning = slider_data['tuning']
                        new_slider.is_show = slider_data['is_show']
                        new_slider.Song = song
                        new_slider.save()
                        # downloader
                        payload.append(Downloader.downloader(slider_data['image_link'],
                                                             downloader_type.slider_song_image.value, 'i',
                                                             new_slider.slider_id))
                    else:
                        # update
                        one_slider = slider.first()
                        slider.update(lyric=slider_data['lyric']) if one_slider.lyric != slider_data['lyric'] else None
                        slider.update(release_date=slider_data['release_date']) if one_slider.release_date != \
                                                                                   slider_data['release_date'] else None
                        slider.update(tarane=slider_data['tarane']) if one_slider.tarane != slider_data[
                            'tarane'] else None
                        slider.update(tuning=slider_data['tuning']) if one_slider.tuning != slider_data[
                            'tuning'] else None
                        slider.update(Song=song) if one_slider.Song != song else None
                        slider.update(is_show=slider_data['is_show']) if one_slider.is_show != slider_data[
                            'is_show'] else None

                        new_image = Downloader.url_name(slider_data['image_link'])
                        old_image = Downloader.url_name(one_slider.image_link)
                        if old_image != new_image:
                            payload.append(Downloader.downloader(slider_data['image_link'],
                                                                 downloader_type.slider_song_image.value,
                                                                 'u', one_slider.slider_id))
            # delete
            slider_exists = SliderSong.objects.filter(Song=song)
            exists_id = set(Id[0] for Id in slider_exists.values_list('slider_id'))
            dels_id = exists_id - slider_id
            for slider_id in dels_id:
                slider = slider_exists.get(slider_id=slider_id)
                remove = Downloader.remove_file(Downloader.url_name(slider.image_link),
                                                downloader_type.slider_song_image.value)
                slider.delete() if remove else None
            return payload
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set slider song :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def set_ads(ads_datas: list):
        try:
            payload = []
            ads_id = set()
            if ads_datas:
                for ads_data in ads_datas:
                    ads_id.add(ads_data['ad_id'])
                    ads = Ads.objects.filter(ad_id=ads_data['ad_id'])
                    if not ads:
                        # set ads
                        new_ads = Ads()
                        new_ads.ad_id = ads_data["ad_id"]
                        new_ads.image_url = Downloader.set_url(ads_data["image_url"])
                        new_ads.click_url = ads_data["click_url"]
                        new_ads.video = Videos.objects.filter(video_id=ads_data["video"]).first() \
                            if ads_data["video"] else None
                        new_ads.is_video_ads = ads_data["is_video_ads"]
                        new_ads.save()
                        # downloader
                        payload.append(
                            Downloader.downloader(ads_data["image_url"], downloader_type.ads_image.value, 'i',
                                                  new_ads.ad_id))
                    else:
                        # update
                        one_ads = ads.first()
                        ads.update(is_video_ads=ads_data["is_video_ads"]) if one_ads.is_video_ads != \
                                                                             ads_data["is_video_ads"] else None
                        if one_ads.video:
                            if ads_data["video"]:
                                ads.update(video=Videos.objects.filter(video_id=ads_data["video"]).first()) \
                                    if one_ads.video.video_id != ads_data["video"] else None
                            else:
                                ads.update(video=None)
                        else:
                            if ads_data["video"]:
                                ads.update(video=Videos.objects.filter(video_id=ads_data["video"]).first())
                            else:
                                ads.update(video=None)

                        new_image = Downloader.url_name(ads_data["image_url"])
                        old_image = Downloader.url_name(one_ads.image_url)
                        if old_image != new_image:
                            payload.append(Downloader.downloader(ads_data["image_url"], downloader_type.ads_image.value,
                                                                 'u', one_ads.ad_id))

            # Delete
            ads_exist = Ads.objects.all()
            id_exist = set(Id[0] for Id in ads_exist.values_list('ad_id'))
            dels_id = id_exist - ads_id
            for ad_id in dels_id:
                ads = ads_exist.get(ad_id=ad_id)
                remove = Downloader.remove_file(Downloader.url_name(ads.image_url), downloader_type.ads_image.value)
                ads.delete() if remove else None
            return payload
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set ads :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def set_slider_home(slider_datas: list):
        try:
            slider_id = set()
            payload = []
            if slider_datas:
                for slider_data in slider_datas:
                    slider_id.add(slider_data['slider_id'])
                    slider = SliderHome.objects.filter(slider_id=slider_data['slider_id'])
                    if not slider:
                        # set
                        new_slider = SliderHome()
                        new_slider.slider_id = slider_data['slider_id']
                        new_slider.type = slider_data['type']
                        new_slider.VideoSlider = SliderVideo.objects.filter(slider_id=slider_data['VideoSlider']). \
                            first() if slider_data['VideoSlider'] else None
                        new_slider.SongSlider = SliderSong.objects.filter(slider_id=slider_data['SongSlider']).first() \
                            if slider_data['SongSlider'] else None
                        if slider_data['AdsSlider']:
                            ads_slider = SetData.add_slider_ads(slider_data['AdsSlider'])
                            new_slider.AdsSlider = ads_slider[0] if ads_slider[0] else None
                            new_slider.name = slider_data['name']
                            payload.append(ads_slider[1]) if ads_slider[1] else None
                        new_slider.save()
                    else:
                        # update
                        one_slider = slider.first()
                        slider.update(type=slider_data['type']) if one_slider.type != slider_data['type'] else None

                        if one_slider.VideoSlider:
                            if slider_data['VideoSlider']:
                                slider.update(VideoSlider=SliderVideo.objects.filter(
                                    slider_id=slider_data['VideoSlider']).first()) \
                                    if one_slider.VideoSlider.slider_id != slider_data['VideoSlider'] else None
                            else:
                                slider.update(VideoSlider=None)
                        else:
                            slider.update(VideoSlider=Videos.objects.filter(
                                slider_id=slider_data['VideoSlider']).first()) \
                                if slider_data['VideoSlider'] else slider.update(VideoSlider=None)

                        if one_slider.SongSlider:
                            if slider_data['SongSlider']:
                                slider.update(SongSlider=SliderSong.objects.filter(
                                    slider_id=slider_data['SongSlider']).first()) \
                                    if one_slider.SongSlider.slider_id != slider_data['SongSlider'] else None
                            else:
                                slider.update(SongSlider=None)
                        else:
                            slider.update(SongSlider=Videos.objects.filter(
                                slider_id=slider_data['SongSlider']).first()) if slider_data['SongSlider'] \
                                else slider.update(SongSlider=None)

                        if one_slider.AdsSlider:
                            if slider_data['AdsSlider']:
                                if one_slider.AdsSlider.slider_id != slider_data['AdsSlider']['slider_id'] or \
                                        one_slider.AdsSlider.image_url != slider_data['AdsSlider']['image_url']:
                                    slider_ads = SetData.add_slider_ads(slider_data['AdsSlider'])
                                    payload.append(slider_ads[1])
                                    slider.update(AdsSlider=slider_ads[0])
                            else:
                                slider.update(AdsSlider=None)
                        else:
                            if slider_data['AdsSlider']:
                                slider_ads = SetData.add_slider_ads(slider_data['AdsSlider'])
                                payload.append(slider_ads[1]) if slider_ads[1] else None
                                slider.update(AdsSlider=slider_ads[0])
                            else:
                                slider.update(AdsSlider=None)
            # Delete
            slider_exist = SliderHome.objects.all()
            id_exist = set(Id[0] for Id in slider_exist.values_list('slider_id'))
            dels_id = id_exist - slider_id
            for slider_id in dels_id:
                slider = slider_exist.get(slider_id=slider_id).delete()
            return payload
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set slider home :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

    @staticmethod
    def add_slider_ads(ads_data: dict):
        try:
            slider_id = set()
            ads = SliderAds()
            payload = {}
            if ads_data:
                slider_id.add(ads_data['slider_id'])
                ads = SliderAds.objects.filter(slider_id=ads_data['slider_id'])
                if not ads:
                    # set ads
                    new_ads = SliderAds()
                    new_ads.slider_id = ads_data["slider_id"]
                    new_ads.image_url = Downloader.set_url(ads_data["image_url"])
                    new_ads.click_url = ads_data["click_url"]
                    new_ads.title = ads_data["title"]
                    new_ads.save()
                    payload = Downloader.downloader(ads_data["image_url"], downloader_type.slider_ads_image.value, 'i',
                                                    new_ads.slider_id)
                    ads = new_ads
                else:
                    # update
                    one_ads = ads.first()
                    ads.update(title=ads_data["title"]) if one_ads.title != ads_data["title"] else None
                    ads.update(click_url=ads_data["click_url"]) if one_ads.title != ads_data["click_url"] else None

                    new_image = Downloader.url_name(ads_data["image_url"])
                    old_image = Downloader.url_name(one_ads.image_url)
                    if old_image != new_image:
                        payload = Downloader.downloader(ads_data["image_url"], downloader_type.slider_ads_image.value,
                                                        'u', one_ads.slider_id)
                    ads = one_ads
                    # delete
            slider_exists = SliderAds.objects.all()
            exist_id = set(Id[0] for Id in slider_exists.values_list('slider_id'))
            dels_id = exist_id - slider_id
            for slider_id in dels_id:
                slider = slider_exists.get(slider_id=slider_id)
                remove = Downloader.remove_file(Downloader.url_name(slider.image_url),
                                                downloader_type.slider_ads_image.value)
                slider.delete() if remove else None
            return ads, payload
        except Exception as e:
            f = open("log.txt", "a+")
            f.write("\r\n " + str(datetime.utcnow()) + " Error set slider ads :" + str(e) + "\r\n")
            f.close()
            return [str(e)]

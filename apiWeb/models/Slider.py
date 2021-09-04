from django.db import models

from enum import Enum
from apiApp.models import Videos, Songs


class SliderType(Enum):
    video = 0
    song = 1
    ads = 2
    video_child = 3


class SliderVideo(models.Model):
    slider_id = models.PositiveIntegerField(primary_key=True, unique=True)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    image_link = models.TextField()
    is_show = models.BooleanField(default=False)
    is_childish = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.video.en_name + "=> is Show:" + str(self.is_show)


class SliderSong(models.Model):
    slider_id = models.PositiveIntegerField(primary_key=True, unique=True)
    image_link = models.TextField()
    lyric = models.TextField(null=True)
    release_date = models.CharField(max_length=200, null=True)
    tarane = models.CharField(max_length=100, null=True)
    tuning = models.CharField(max_length=100, null=True)
    is_show = models.BooleanField(default=False)
    Song = models.ForeignKey(Songs, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.Song.en_name + "=> is Show:" + str(self.is_show)


class SliderAds(models.Model):
    slider_id = models.PositiveIntegerField(primary_key=True, unique=True)
    image_url = models.TextField()
    click_url = models.TextField()
    title = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class SliderHome(models.Model):
    type_choices = [
        (SliderType.video.value, SliderType.video.name),
        (SliderType.song.value, SliderType.song.name),
        (SliderType.ads.value, SliderType.ads.name),
        (SliderType.video_child.value, SliderType.video_child.name),
    ]
    slider_id = models.PositiveIntegerField(primary_key=True, unique=True)
    type = models.SmallIntegerField(choices=type_choices)
    VideoSlider = models.ForeignKey(SliderVideo, on_delete=models.CASCADE, null=True, blank=True)
    SongSlider = models.ForeignKey(SliderSong, on_delete=models.CASCADE, null=True, blank=True)
    AdsSlider = models.ForeignKey(SliderAds, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, default="test1")

    def __str__(self):
        return self.name

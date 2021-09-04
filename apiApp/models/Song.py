from enum import Enum

from django.db import models


class Singer_Channel(models.Model):
    singer_id = models.PositiveIntegerField(primary_key=True, unique=True)
    fa_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    image_link = models.TextField()
    is_channel = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Singer Or Channel"

    def __str__(self):
        if self.is_channel:
            return self.fa_name + "=>  is channel"
        else:
            return self.fa_name


class Album(models.Model):
    album_id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    image_link = models.TextField()
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Album"

    def __str__(self):
        return self.name


class Songs(models.Model):
    song_id = models.PositiveIntegerField(primary_key=True, unique=True)
    fa_name = models.CharField(max_length=100)
    en_name = models.CharField(max_length=100)
    image_link = models.TextField()
    is_active_image = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    min_age = models.IntegerField(default=-1)
    description = models.TextField()
    singer = models.ForeignKey(Singer_Channel, on_delete=models.CASCADE, blank=True, null=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    length = models.IntegerField()
    link = models.TextField()
    is_active_link = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now=True)
    is_podcast = models.BooleanField(default=False)
    is_childish = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Songs"

    def __str__(self):
        if self.is_podcast:
            return self.en_name + ' => is podcast'
        elif self.is_childish:
            return self.en_name + ' => is Childish'
        else:
            return self.en_name


class SongStyles(models.Model):
    style_id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    songs = models.ManyToManyField(to=Songs)

    class Meta:
        verbose_name_plural = "Song Styles"

    def __str__(self):
        return self.name


class OrderByPlaylist(Enum):
    random = 0
    latest = 1
    most_visited = 2
    en_name = 3


class Playlists(models.Model):
    type_choices = [
        (OrderByPlaylist.random.value, OrderByPlaylist.random.name),
        (OrderByPlaylist.latest.value, OrderByPlaylist.latest.name),
        (OrderByPlaylist.most_visited.value, OrderByPlaylist.most_visited.name),
        (OrderByPlaylist.en_name.value, OrderByPlaylist.en_name.name),
    ]
    playlist_id = models.PositiveIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    cover = models.TextField()
    songs = models.ManyToManyField(to=Songs, blank=True)
    is_active = models.BooleanField(default=False)
    sort_by = models.SmallIntegerField(choices=type_choices, default=1)

    class Meta:
        verbose_name_plural = "Playlists"

    def __str__(self):
        return self.name

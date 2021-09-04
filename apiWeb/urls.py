from django.urls import path

from .views.Home import *
from .views.Song import *
from .views.video import *

urlpatterns = [
    path('home/main-slider', home_slider.as_view()),
    path('home/videos', home_video.as_view()),
    path('home/songs', home_song.as_view()),
    path('home/podcasts', home_podcast.as_view()),
    path('home/ads', home_ads.as_view()),
    path('search', search.as_view()),

    path('movies/slider', movies_slider.as_view()),
    path('movies/cat', movies_category.as_view()),
    path('movies/cat/<int:cat_id>', movies_category_video.as_view()),
    path('movies/newVideo', movies_new_video.as_view()),
    path('movies/mosteVisitedVideo', movies_most_visited_video.as_view()),
    path('movies/ads', movies_ads.as_view()),
    path('movies/videoAds', movies_video_ads.as_view()),
    path('movies/<str:video_slug>', one_video.as_view()),

    path('songs/slider', songs_slider.as_view()),
    path('songs/latest', songs_latest.as_view()),
    path('songs/popular', songs_popular.as_view()),
    path('songs/podcasts/latest', songs_podcasts_latest.as_view()),
    path('songs/podcasts/popular', songs_podcasts_popular.as_view()),
    path('songs/playlists', songs_playlists.as_view()),
    path('songs/playlists/all', songs_all_playlists.as_view()),
    path('songs/playlist/<int:playlist_id>', playlist_songs.as_view()),
    path('songs/singers', songs_singers.as_view()),
    path('songs/singers/all', songs_all_singers.as_view()),
    path('songs/singers/<int:singer_id>', singer_songs.as_view()),
    path('songs/channels', songs_channels.as_view()),
    path('songs/channels/all', songs_all_channel.as_view()),
    path('songs/channel/<int:channel_id>', channel_songs.as_view()),
    path('songs/ads', songs_ads.as_view()),
]

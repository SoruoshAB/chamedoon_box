from django.urls import path

from .views import *

urlpatterns = [
    path('Home', Home.as_view()),
    path('child', child.as_view()),
    path('search', search.as_view()),

    path('Songs', Music.as_view()),
    path('AllSongs/<int:page>', get_all_songs.as_view()),
    path('AllChannel/<int:page>', get_all_channel.as_view()),
    path('AllPodcast/<int:page>', get_all_podcast.as_view()),
    path('singer_channel/<int:singer_channel_id>', get_singer_channel.as_view()),
    path('singer_channel/<int:singer_channel_id>/single_song_more/<int:page>',
         get_singer_channel_single_song.as_view()),
    path('singer_channel/<int:singer_channel_id>/popular_song_more/<int:page>',
         get_singer_channel_popular_song.as_view()),
    path('AddViewSongCount/<int:song_id>', AddViewSongCount.as_view()),
    path('AllSinger/<int:page>', get_all_singer.as_view()),
    path('PlayList/<int:playlist_id>', get_playlist.as_view()),
    path('PlayList/<int:playlist_id>/single_song_more/<int:page>', get_single_songs_playlist.as_view()),
    path('PlayList/<int:playlist_id>/popular_song_more/<int:page>', get_popular_songs_playlist.as_view()),

    path('Movies', Movies.as_view()),
    path('Video/<int:video_id>', Video.as_view()),
    path('AllVideo/<int:page>', get_all_videos.as_view()),
    path('CatVideos/<int:cat_id>/<int:page>', get_videos_category.as_view()),
    path('GenreVideos/<int:genre_id>/<int:page>', get_videos_genre.as_view()),
    path('ActorVideos/<int:actor_id>/<int:page>', get_videos_actor.as_view()),
    path('VideoComments/<int:video_id>', video_comments.as_view()),
    path('VideoComments/<int:video_id>/<int:page>', video_comments.as_view()),
    path('AddViewVidoeCount/<int:video_id>', AddViewVideoCount.as_view()),
]

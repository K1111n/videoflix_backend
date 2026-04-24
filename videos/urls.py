from django.urls import path
from .views import VideoListView, HlsPlaylistView, HlsSegmentView

urlpatterns = [
    path('video/', VideoListView.as_view(), name='video_list'),
    path('video/<int:movie_id>/<str:resolution>/index.m3u8', HlsPlaylistView.as_view(), name='hls_playlist'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', HlsSegmentView.as_view(), name='hls_segment'),
]

from pathlib import Path
from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Video
from .serializers import VideoSerializer


class VideoListView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class HlsPlaylistView(APIView):
    def get(self, request, movie_id, resolution):
        playlist_path = self._get_file_path(movie_id, resolution, 'index.m3u8')
        return FileResponse(open(playlist_path, 'rb'), content_type='application/vnd.apple.mpegurl')

    def _get_file_path(self, movie_id, resolution, filename):
        path = Path(settings.MEDIA_ROOT) / 'videos' / 'hls' / str(movie_id) / resolution / filename
        if not path.exists():
            raise Http404
        return path


class HlsSegmentView(APIView):
    def get(self, request, movie_id, resolution, segment):
        segment_path = self._get_file_path(movie_id, resolution, segment)
        return FileResponse(open(segment_path, 'rb'), content_type='video/MP2T')

    def _get_file_path(self, movie_id, resolution, filename):
        path = Path(settings.MEDIA_ROOT) / 'videos' / 'hls' / str(movie_id) / resolution / filename
        if not path.exists():
            raise Http404
        return path

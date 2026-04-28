from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Video
from .serializers import VideoSerializer


class VideoListView(ListAPIView):
    """Return a list of all videos ordered by creation date."""

    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class HlsPlaylistView(APIView):
    """Serve the HLS m3u8 playlist file for a given video and resolution."""

    def get(self, request, movie_id, resolution):
        """Return the m3u8 playlist file as a streaming response."""
        playlist_path = self._get_file_path(movie_id, resolution, 'index.m3u8')
        return FileResponse(open(playlist_path, 'rb'), content_type='application/vnd.apple.mpegurl')

    def _get_file_path(self, movie_id, resolution, filename):
        """Build and validate the filesystem path for the requested HLS file."""
        path = Path(settings.MEDIA_ROOT) / 'videos' / 'hls' / str(movie_id) / resolution / filename
        if not path.exists():
            raise Http404
        return path


class HlsSegmentView(APIView):
    """Serve a single HLS .ts segment for a given video and resolution."""

    def get(self, request, movie_id, resolution, segment):
        """Return the requested .ts segment as a streaming response."""
        segment_path = self._get_file_path(movie_id, resolution, segment)
        return FileResponse(open(segment_path, 'rb'), content_type='video/MP2T')

    def _get_file_path(self, movie_id, resolution, filename):
        """Build and validate the filesystem path for the requested HLS file."""
        path = Path(settings.MEDIA_ROOT) / 'videos' / 'hls' / str(movie_id) / resolution / filename
        if not path.exists():
            raise Http404
        return path

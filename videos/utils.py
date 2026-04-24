import subprocess
from pathlib import Path


RESOLUTIONS = {
    '480p':  {'size': '854x480',  'bitrate': '800k'},
    '720p':  {'size': '1280x720', 'bitrate': '2500k'},
    '1080p': {'size': '1920x1080','bitrate': '5000k'},
}


def get_output_dir(video):
    from django.conf import settings
    return Path(settings.MEDIA_ROOT) / 'videos' / 'hls' / str(video.id)


def build_ffmpeg_command(input_path, output_dir, resolution, config):
    playlist = output_dir / 'index.m3u8'
    segment = output_dir / '%03d.ts'
    return [
        'ffmpeg', '-i', str(input_path),
        '-vf', f"scale={config['size']}",
        '-b:v', config['bitrate'],
        '-hls_time', '10',
        '-hls_playlist_type', 'vod',
        '-hls_segment_filename', str(segment),
        str(playlist),
        '-y',
    ]


def convert_to_hls(video):
    input_path = Path(video.video_file.path)
    for resolution, config in RESOLUTIONS.items():
        output_dir = get_output_dir(video) / resolution
        output_dir.mkdir(parents=True, exist_ok=True)
        command = build_ffmpeg_command(input_path, output_dir, resolution, config)
        subprocess.run(command, check=True)

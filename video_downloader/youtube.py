from pydantic import BaseModel
from typing import List
from pytube import YouTube, Playlist
from moviepy.editor import VideoFileClip
import os
import re
from urllib.parse import parse_qs, urlparse

class VideoRequest(BaseModel):
    url: str

class MultipleVideoRequest(BaseModel):
    urls: List[str]

class PlaylistRequest(BaseModel):
    url: str
    
def download_single_video(video_request: VideoRequest):
    youtube = YouTube(video_request.url)
    video = youtube.streams.get_highest_resolution()
    filesize = video.filesize / (1024 * 1024)
    title = video.title
    video.download(output_path="./downloads", filename=title, skip_existing=False)
    return {"status": "success", "title": title, "size": f"{filesize:.2f} MB"}


def download_multiples_videos(video_request: MultipleVideoRequest):
    responses = []
    for url in video_request.urls:
        youtube = YouTube(url)
        video = youtube.streams.get_highest_resolution()
        filesize = video.filesize / (1024 * 1024)
        title = video.title
        video.download(output_path="./downloads", filename=title, skip_existing=False)
        responses.append({"status": "success", "title": title, "size": f"{filesize:.2f} MB"})
    return responses


async def download_playlist(playlist_request: PlaylistRequest):
    playlist_url = playlist_request.url
    parsed_url = urlparse(playlist_url)
    query_params = parse_qs(parsed_url.query)
    if "list" not in query_params:
        return {"message": "Invalid playlist URL"}

    playlist_id = query_params["list"][0]
    playlist = Playlist(f"https://www.youtube.com/playlist?list={playlist_id}")
    video_ids = [re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url).group(1) for url in playlist.video_urls]
    responses = []
    for video_id in video_ids:
        try:
            video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            title = video.title
            video_stream = video.streams.get_highest_resolution()
            filename = f"{title}.mp4"
            filepath = os.path.join("./downloads", filename)
            video_stream.download(output_path="./downloads", filename=title, skip_existing=False)
            clip = VideoFileClip(filepath)
            audio_file = os.path.join("./downloads", f"{title}.mp3")
            clip.audio.write_audiofile(audio_file)
            clip.close()
            filesize = video_stream.filesize / (1024 * 1024)
            responses.append({"status": "success", "title": title, "size": f"{filesize:.2f} MB"})
        except Exception as e:
            responses.append({"status": "failure", "title": title, "error": str(e)})
    return responses
from pydantic import BaseModel
from typing import List
from pytube import YouTube

class VideoRequest(BaseModel):
    url: str

class MultipleVideoRequest(BaseModel):
    urls: List[str]
    
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
from fastapi import FastAPI, HTTPException
from video_downloader.youtube import *
from url_shortener.shortener import *
from password_generator.pass_generator import *
from images_compressor.img_compressor import *
from file_mover.file_mover import *

from pytube import Playlist, YouTube
from moviepy.editor import VideoFileClip
from youtube_dl import YoutubeDL
from youtube_dl.utils import ExtractorError, DownloadError

from tqdm import tqdm
from pydantic import BaseModel
import os
import re
import subprocess
from urllib.parse import urlparse, parse_qs


class PlaylistRequest(BaseModel):
    url: str


app = FastAPI()


@app.get("/")
def root():
    return {"ping": "pong"}


@app.post("/download-single", tags=["Youtube"])
async def download_single(url: str):
    video_request = VideoRequest(url=url)
    response = download_single_video(video_request)
    return response


@app.post("/download-multiples", tags=["Youtube"])
async def download_multiple(video_request: MultipleVideoRequest):
    response = download_multiples_videos(video_request)
    return response


@app.post("/download-playlist", tags=["Youtube"])
async def download_playlist_handler(video_request: VideoRequest):
    playlist_url = video_request.url

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "./downloads/%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
            playlist_title = ydl.extract_info(
                playlist_url, download=False).get("title", "playlist")
            playlist_size = sum(os.path.getsize(
                f"./downloads/{filename}") for filename in os.listdir("./downloads")) / (1024 * 1024)
            return {"status": "success", "playlist_title": playlist_title, "size": f"{playlist_size:.2f} MB"}
    except ExtractorError as e:
        # Handle errors raised by youtube-dl extractors
        raise HTTPException(status_code=400, detail=str(e))
    except DownloadError as e:
        # Handle errors raised by youtube-dl downloader
        print(f"Failed to download video: {str(e)}")
        pass
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=400, detail=str(e))

    # If we reach here, we had an error downloading at least one video, so we need to skip those that fail
    try:
        with YoutubeDL(ydl_opts) as ydl:
            playlist_dict = ydl.extract_info(
                playlist_url, download=False)
            playlist_title = playlist_dict.get("title", "playlist")
            playlist_urls = [video["webpage_url"]
                             for video in playlist_dict["entries"] if video.get("webpage_url")]
            for url in playlist_urls:
                try:
                    ydl.download([url])
                except ExtractorError as e:
                    print(f"Failed to download {url}: {e}")
                    continue
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=400, detail=str(e))

    playlist_size = sum(os.path.getsize(
        f"./downloads/{filename}") for filename in os.listdir("./downloads")) / (1024 * 1024)
    return {"status": "success", "playlist_title": playlist_title, "size": f"{playlist_size:.2f} MB"}

# @app.post("/download-single-mp3", tags=["Youtube"])
# async def download_single_mp3_handler(video_request: VideoRequest):
#     video_url = video_request.url
#     video_id_match = re.search(r"v=([0-9A-Za-z_-]{11})", video_url)
#     if not video_id_match:
#         return {"message": "Invalid video URL"}

#     video_id = video_id_match.group(1)
#     try:
#         video = YouTube(f"https://www.youtube.com/watch?v={video_id}")
#         title = video.title
#         audio_stream = video.streams.filter(only_audio=True).first()
#         filename = f"{title}.mp3"
#         filepath = os.path.join("./downloads", filename)
#         audio_stream.download(output_path="./downloads", filename=title, skip_existing=False)
#         response = {"status": "success", "title": title, "size": f"{audio_stream.filesize / (1024 * 1024):.2f} MB"}
#     except Exception as e:
#         response = {"status": "failure", "title": title, "error": str(e)}

#     return response


@app.post("/download-single-mp3", tags=["Youtube"])
async def download_single_mp3_handler(video_request: VideoRequest):
    video_url = video_request.url
    video_id = video_url.split("=")[1]
    try:
        output_dir = "./downloads"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        cmd = f"youtube-dl -x --audio-format mp3 -o '{output_dir}/%(title)s.%(ext)s' https://www.youtube.com/watch?v={video_id}"
        subprocess.run(cmd, shell=True, check=True)
        title = subprocess.check_output(
            f"youtube-dl --get-title https://www.youtube.com/watch?v={video_id}", shell=True, text=True)
        title = title.strip()
        filesize = os.path.getsize(f"{output_dir}/{title}.mp3") / (1024 * 1024)
        response = {"status": "success", "title": title,
                    "size": f"{filesize:.2f} MB"}
    except subprocess.CalledProcessError as e:
        response = {"status": "failure", "title": "", "error": str(e)}

    return response


@app.post("/shorten", tags=["Url Shortener"])
def create_short_url(url: str):
    return shorten_url(url)


@app.get("/{short_url}", tags=["Url Shortener"])
def redirect_url(short_url: int):
    try:
        return redirect(short_url)
    except NotFoundUrl:
        return {"message": "Short URL not found"}


@app.post("/password", tags=["Password Generator"])
async def password(request: PasswordGeneratorRequest):
    return generate_password(request)


@app.post("/compress", tags=["Images Compressor"])
async def compress_endpoint(file: UploadFile = File(...)):
    result = compress_image(file)
    return result


@app.post("/move_files", tags=["File Mover"])
async def move_files_endpoint():
    move_files()
    return {"message": "Files moved successfully!"}

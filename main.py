from fastapi import FastAPI
from video_downloader.youtube import * 
from url_shortener.shortener import *
from password_generator.pass_generator import *

app = FastAPI()

@app.get("/")
def root():
    return {"ping": "pong"}

@app.post("/download-single", tags=["Video Downloader"])
async def download_single(url: str):
    video_request = VideoRequest(url=url)
    response = download_single_video(video_request)
    return response

@app.post("/download-multiples", tags=["Video Downloader"])
async def download_multiple(video_request: MultipleVideoRequest):
    response = download_multiples_videos(video_request)
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
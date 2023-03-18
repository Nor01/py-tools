from fastapi import FastAPI
from video_downloader.youtube import * 
from url_shortener.shortener import *
from password_generator.pass_generator import *
from images_compressor.img_compressor import *
from file_mover.file_mover import *

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
async def download_playlist_handler(playlist_request: PlaylistRequest):
    response = await download_playlist(playlist_request)
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
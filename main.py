from fastapi import FastAPI
from video_downloader.youtube import * 


app = FastAPI()

@app.get("/")
def root():
    return {"ping": "pong"}

@app.post("/download-single")
async def download_single(url: str):
    video_request = VideoRequest(url=url)
    response = download_single_video(video_request)
    return response

@app.post("/download-multiples")
async def download_multiple(video_request: MultipleVideoRequest):
    response = download_multiples_videos(video_request)
    return response
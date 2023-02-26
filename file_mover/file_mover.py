from PIL import Image
import os

DOWNLOAD_FOLDER = "/Users/maino/Downloads/"
PICTURES_FOLDER = "/Users/maino/Downloads/Pictures/"
VIDEOS_FOLDER = "/Users/maino/Downloads/videos/"
MUSIC_FOLDER = "/Users/maino/Downloads/Music/"
PDF_FOLDER = "/Users/maino/Downloads/PDF/"

def move_files():
    for filename in os.listdir(DOWNLOAD_FOLDER):
        name, extension = os.path.splitext(filename)

        if extension in [".jpg", ".jpeg", ".png"]:
            picture = Image.open(DOWNLOAD_FOLDER + filename)
            picture.save(DOWNLOAD_FOLDER + filename, optimize=True, quality=60)
            os.rename(DOWNLOAD_FOLDER + filename, PICTURES_FOLDER + filename)

        if extension in [".mp3"]:
            os.rename(DOWNLOAD_FOLDER + filename, MUSIC_FOLDER + filename)
        
        if extension in [".mp4"]:
            os.rename(DOWNLOAD_FOLDER + filename, VIDEOS_FOLDER + filename)
        
        if extension in [".pdf"]:
            os.rename(DOWNLOAD_FOLDER + filename, PDF_FOLDER + filename)
    
    return {"message": "Files moved successfully!"}
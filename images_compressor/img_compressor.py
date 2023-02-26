from fastapi import File, UploadFile
from PIL import Image
import os

def compress_image(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1]
    if extension not in ["jpg", "jpeg", "png"]:
        return {"error": "File format not supported. Please provide a jpg, jpeg, or png file."}
    
    download_folder = "./downloads/"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    compressed_filename = "compressed_" + file.filename
    compressed_path = os.path.join(download_folder, compressed_filename)
    
    with Image.open(file.file) as img:
        img.save(compressed_path, optimize=True, quality=60)
    
    return {"message": "Image compressed successfully.", "path": compressed_path}
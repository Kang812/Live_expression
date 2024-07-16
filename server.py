from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import os
import uvicorn

app = FastAPI()

UPLOAD_DIR = "uploads"
RESULT_DIR = "results"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

@app.post("/upload")
async def upload_files(image: UploadFile = File(...), video: UploadFile = File(...)):
    image_path = os.path.join(UPLOAD_DIR, image.filename)
    video_path = os.path.join(UPLOAD_DIR, video.filename)
    result_path = os.path.join(RESULT_DIR, "result.mp4")

    with open(image_path, "wb") as img_file:
        shutil.copyfileobj(image.file, img_file)

    with open(video_path, "wb") as vid_file:
        shutil.copyfileobj(video.file, vid_file)

    # Here you should add your processing logic and generate result video
    # For this example, we are just copying the video as the result
    shutil.copy(video_path, result_path)

    return FileResponse(path=result_path, filename="result.mp4", media_type="video/mp4")

if __name__ == "__main__":
    uvicorn.run("server:app", reload=True)
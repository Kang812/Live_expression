import uvicorn
import os
import shutil
import os.path as osp
import sys
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse, HTMLResponse
sys.path.append("/workspace/Live_expression/LivePortrait/")
from src.config.argument_config import ArgumentConfig
from src.config.inference_config import InferenceConfig
from src.config.crop_config import CropConfig
from src.live_portrait_pipeline import LivePortraitPipeline
import tyro
import subprocess


def partial_fields(target_class, kwargs):
    return target_class(**{k: v for k, v in kwargs.items() if hasattr(target_class, k)})

def fast_check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except:
        return False

def fast_check_args(args: ArgumentConfig):
    if not osp.exists(args.source_image):
        raise FileNotFoundError(f"source image not found: {args.source_image}")
    if not osp.exists(args.driving_info):
        raise FileNotFoundError(f"driving info not found: {args.driving_info}")
    
app = FastAPI()

UPLOAD_DIR = "uploads"
RESULT_DIR = "results"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

@app.post("/upload")
async def upload_files(image: UploadFile = File(...), 
                       video: UploadFile = File(...),
                       flag_eye_retargeting: bool = Form(False),
                       flag_lip_retargeting: bool = Form(False),
                       flag_stitching: bool = Form(True),
                       flag_relative_motion: bool = Form(True)):
    
    image_path = os.path.join(UPLOAD_DIR, image.filename)
    video_path = os.path.join(UPLOAD_DIR, video.filename)
    result_path = os.path.join(RESULT_DIR, "result.mp4")

    #print(flag_eye_retargeting)
    #print(flag_lip_retargeting)
    #print(flag_stitching)
    #print(flag_relative_motion)

    with open(image_path, "wb") as img_file:
        shutil.copyfileobj(image.file, img_file)

    with open(video_path, "wb") as vid_file:
        shutil.copyfileobj(video.file, vid_file)

    tyro.extras.set_accent_color("bright_cyan")
    args = tyro.cli(ArgumentConfig)
    
    args.source_image = image_path
    args.driving_info = video_path
    args.output_dir = RESULT_DIR  # Adjusted to directory instead of file
    args.flag_eye_retargeting = flag_eye_retargeting
    args.flag_lip_retargeting = flag_lip_retargeting
    args.flag_stitching = flag_stitching
    args.flag_relative_motion = flag_relative_motion

    # specify configs for inference
    inference_cfg = partial_fields(InferenceConfig, args.__dict__)
    crop_cfg = partial_fields(CropConfig, args.__dict__)

    live_portrait_pipeline = LivePortraitPipeline(
        inference_cfg=inference_cfg,
        crop_cfg=crop_cfg
    )

    live_portrait_pipeline.execute(args)
    
    # Construct the result filename
    image_filename = image_path.split("/")[-1].split(".")[0]
    video_filename = video_path.split("/")[-1]
    result_filename = image_filename + "--" + video_filename
    
    return {"result_filename": result_filename}

@app.get("/results/{filename}")
async def download_file(filename: str):
    file_path = os.path.join("results", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")
    
@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/", response_class=HTMLResponse)
async def main():
    with open("./index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

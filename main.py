from fastapi import FastAPI , status , HTTPException
from pydantic import BaseModel
from loguru import logger

from time import strftime
from time import time
from src.utils.preprocess import CropAndExtract
from src.test_audio2coeff import Audio2Coeff  
from src.facerender.animate_onnx import AnimateFromCoeff
from src.generate_batch import get_data
from src.generate_facerender_batch import get_facerender_data
from src.utils.init_path import init_path

import requests
import json
import os, sys
import base64
import os

tts_service = os.getenv("TTS_SERVER")
pic_path ="./sadtalker_default.jpeg"
facerender_batch_size = 10
sadtalker_paths = init_path("./checkpoints", os.path.join("/home/SadTalker", 'src/config'), "256", False, "full")

preprocess_model = CropAndExtract(sadtalker_paths, "cuda")
audio_to_coeff = Audio2Coeff(sadtalker_paths, "cuda")
animate_from_coeff = AnimateFromCoeff(sadtalker_paths, "cuda")

app = FastAPI()

class Words(BaseModel):
    words: str


@app.post("/pipeline")
async def predict_image(items:Words):
    save_dir = os.path.join("/home/SadTalker/results", strftime("%Y_%m_%d_%H.%M.%S"))
    """
    从语音服务器获取语音内容
    """
    try:
        tts_json = json.dumps({"text": items.words,"model_id": "zhisha"})
        tts_result = requests.post(url=tts_service,data=tts_json).json()["wav"]
        print(tts_result)
        audio_data = base64.b64decode(tts_result)
        audio_path = "/home/SadTalker/001.wav"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(audio_data)
    except Exception as e:
        errors = str(e)
        mod_errors = errors.replace('"', '**').replace("'", '**')
        logger.error(mod_errors)
        message = {
            "err_no": "400",
            "err_msg": mod_errors
            }
        json_data = json.dumps(message)
        json_data = json_data.replace("'", '"')
        return json_data

    first_frame_dir = os.path.join(save_dir, 'first_frame_dir')
    os.makedirs(first_frame_dir, exist_ok=True)
    first_coeff_path, crop_pic_path, crop_info =  preprocess_model.generate(pic_path, first_frame_dir, "full", source_image_flag=True)
    ref_eyeblink_coeff_path=None
    ref_pose_coeff_path=None
    batch = get_data(first_coeff_path, audio_path, "cuda", ref_eyeblink_coeff_path, still=True)
    coeff_path = audio_to_coeff.generate(batch, save_dir, 0, ref_pose_coeff_path)

    data = get_facerender_data(coeff_path, crop_pic_path, first_coeff_path, audio_path, 
                                facerender_batch_size, None, None, None,
                                expression_scale=1, still_mode=True, preprocess="full")
    start_time = time()
    video_path = animate_from_coeff.generate_deploy(data, save_dir, pic_path, crop_info, \
                                enhancer="gfpgan", background_enhancer=None, preprocess="full")
    end_time = time()
    logger.error(f"time: {end_time-start_time}")
    with open(video_path, "rb") as file:
            # 将视频内容进行 base64 编码
            video_data = base64.b64encode(file.read()).decode("utf-8")
        
        # 构建响应数据
    response = {
            "video_base64": video_data
        }
        
    return response
    
    
        
@app.get("/health")
async def health_check():
    try:
        logger.info("health 200")
        return status.HTTP_200_OK

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@app.get("/health/inference")
async def health_check():
    try:
        logger.info("health 200")
        return status.HTTP_200_OK

    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
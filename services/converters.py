import tempfile

import cv2
import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from gtts import gTTS
from PIL import Image

from app.settings import settings


def convert_images_to_text(images: list[Image]) -> list[str]:
    model = VisionEncoderDecoderModel.from_pretrained(settings.huggingface_model)
    feature_extractor = ViTImageProcessor.from_pretrained(settings.huggingface_model)
    tokenizer = AutoTokenizer.from_pretrained(settings.huggingface_model)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    gen_kwargs = {
        'max_length': settings.huggingface_desc_length, 
        'num_beams': settings.huggingface_beams_number
    }

    pixel_values = feature_extractor(images=images, return_tensors='pt').pixel_values
    pixel_values = pixel_values.to(device)

    output_ids = model.generate(pixel_values, **gen_kwargs)

    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
 
    return preds


def convert_text_to_audio(text: str) -> bytes:
    with tempfile.NamedTemporaryFile() as temp_file:
        tts = gTTS(text=text, lang=settings.audio_lang)
        tts.save(temp_file.name)

        with open(temp_file.name, 'rb') as audio_file:
            return audio_file.read()


def convert_video_to_images(video: bytes):
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file.write(video)
        
        video_cap = cv2.VideoCapture(temp_file.name)
        
        frame_count = 0
        frame_rate = settings.video_capture_rate
        frame_skip_interval = int(round(video_cap.get(cv2.CAP_PROP_FPS) / frame_rate))
        
        images = []        
        while video_cap.isOpened():
            ret, frame = video_cap.read()
            
            if not ret:
                break
            
            frame_count += 1
            if frame_count % frame_skip_interval != 0:
                continue
            
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            images.append(image)
        
        return images
        

    
        
        


    
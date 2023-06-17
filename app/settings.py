from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    tg_bot_token: SecretStr
    
    # chatgpt
    openai_token: SecretStr
    openai_model: str = 'gpt-3.5-turbo'
    openai_role: str = 'user'
    
    # image-to-text model
    huggingface_model: str = 'nlpconnect/vit-gpt2-image-captioning'
    huggingface_desc_length: int = 10
    huggingface_beams_number: int = 4
    
    # audio from text getting
    audio_lang: str = 'en'
    
    # image extraction
    video_capture_rate: int = 10
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        

settings = Settings()
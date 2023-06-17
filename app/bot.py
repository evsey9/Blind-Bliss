import logging

from telebot import TeleBot
from telebot.types import Message

from settings import settings
from services.converters import (
    convert_video_to_images,
    convert_images_to_text, 
    convert_text_to_audio
)
from services import openai_api


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

bot = TeleBot(settings.tg_bot_token.get_secret_value())


@bot.message_handler(content_types=['video'])
def get_video_description(message: Message):
    bot.send_message(message.chat.id, 'Getting audio description please wait...')
    
    video_info = bot.get_file(message.video.file_id)
    video = bot.download_file(video_info.file_path)

    logger.info('Extracting images from video')
    images = convert_video_to_images(video)
    
    logger.info(f'Extracting text from {len(images)} images')
    images_descriptions = convert_images_to_text(images)
    
    logger.info('Getting story from text')
    summary = ' '.join(images_descriptions)
    story = openai_api.send_request(
        "Given the descriptions of video's frames, "
        "please construct one precise and exhaustive "
        "description of the whole video, including the "
        f"plot and crucial details. Descriptions of frames are: {summary}"
    )
    
    logger.info('Getting audio from text')
    audio = convert_text_to_audio(story)
    
    bot.send_audio(message.chat.id, audio)
    
    
@bot.message_handler(commands=['prob'])
def get_prob_alive(message: Message):
    bot.send_message(message.chat.id, 'I am alive')


if __name__ == '__main__':
    bot.polling(none_stop=True)

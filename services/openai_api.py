import openai

from app.settings import settings


openai.api_key = settings.openai_token.get_secret_value()


def send_request(text: str) -> str:
    response = openai.ChatCompletion.create(
        model=settings.openai_model,
        messages=[{'role': settings.openai_role, 'content': text}]
    )
    
    result = ''
    for choice in response.choices:
        result += choice.message.content
    
    return result
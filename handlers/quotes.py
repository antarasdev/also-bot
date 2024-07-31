import requests

from aiogram.filters import Command
from aiogram import Router, types
from config import config
from aiogram import Bot


bot = Bot(token=config.API_TOKEN)

quotes = Router()


def get_quote() -> str:
    """
    Получает цитату из API Forismatic.

    Returns:
        str: Строка с цитатой и автором.
    """
    url = "https://api.forismatic.com/api/1.0/"
    params = {
        "method": "getQuote",
        "format": "json",
        "lang": "ru"
    }
    response = requests.get(url, params=params)
    data = response.json()
    quote_text = data['quoteText'].strip()
    quote_author = data['quoteAuthor'].strip()
    if quote_author:
        return f'💬 Цитата дня:\n\n "{quote_text}"\n\n— {quote_author}'
    else:
        return f'{quote_text}\n\n— Неизвестный автор'


@quotes.message(Command('quote'))
async def send_quote():
    """
     Обрабатывает команду /quote и отправляет цитату в чат.
    """
    quote_text = get_quote()
    await bot.send_message(chat_id=config.CHAT_ID, text=quote_text)

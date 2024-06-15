from pymorphy3 import MorphAnalyzer

from bot import bot
from utils.csv_utils import decline_name_parts, capitalize_name, decline_number


async def send_congratulations(chat_id, full_name, department, years):
    morph = MorphAnalyzer()
    declined_name = decline_name_parts(full_name, morph)
    capitalized_name = capitalize_name(declined_name)
    declined_years = decline_number(years, morph)
    await bot.send_message(
        chat_id, f"Поздравляем {capitalized_name} из отдела {department}! Вы с нами уже {declined_years}!"
    )

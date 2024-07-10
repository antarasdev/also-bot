from pymorphy3 import MorphAnalyzer

from bot import bot
from utils.csv_utils import decline_name_parts, capitalize_name, decline_number


async def send_congratulations(chat_id: int, username: str, department: str, years: int) -> None:
    """
    Отправляет поздравительное сообщение пользователю
    Args:
        chat_id (int): ID чата, в который отправляется сообщение
        username (str): Логин пользователя, которому отправляется поздравление
        department (str): Департамент пользователя, которому отправляется поздравление
        years (int): Количество лет, которое пользователь работает в компании

    Returns:
        None
    """
    morph = MorphAnalyzer()
    declined_years = decline_number(years, morph)
    await bot.send_message(
        chat_id, f"Поздравляем {username} {department}! Вы с нами уже {declined_years}!"
    )

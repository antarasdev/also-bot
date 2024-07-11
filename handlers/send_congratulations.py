from utils.csv_utils import decline_name_parts, capitalize_name, decline_number
from config.config import CHAT_ID, API_TOKEN
from aiogram import Bot


bot = Bot(token=API_TOKEN)


async def send_congratulations(username: str, department: str, years: str) -> None:
    """
    Отправляет поздравительное сообщение пользователю
    Args:
        chat_id (CHAT_ID): ID чата, в который отправляется сообщение
        username (str): Логин пользователя, которому отправляется поздравление
        department (str): Департамент пользователя, которому отправляется поздравление
        years (str): Количество лет, которое пользователь работает в компании

    Returns:
        None
    """
    declined_years = decline_number(years)
    await bot.send_message(CHAT_ID, f"Поздравляем {username} {department}! Вы с нами уже {declined_years}!")

import datetime

from utils.csv_utils import decline_name_parts, capitalize_name, decline_number, read_data
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
    await bot.send_message(
        CHAT_ID,
        f"{username} | {department}. Поздравляем! Вы с нами уже {declined_years}!🎉🎉🎉")


async def check_anniversary():
    """
    Проверяет, есть ли сегодня день рождения у кого-то из сотрудников
    и отправляет поздравления, если есть
    """
    logging.info("Checking anniversary")
    today = datetime.date.today()
    df = read_data()
    for index, row in df.iterrows():
        start_date = datetime.datetime.strptime(row['start_date'], '%d.%m.%Y').date()
        anniversary_date = datetime.date(today.year, start_date.month, start_date.day)
        if anniversary_date == today:
            years_in_company = today.year - start_date.year
            await send_congratulations(
                username=row['username'],
                department=row['department'],
                years=years_in_company
            )
            await asyncio.sleep(1)

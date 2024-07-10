import asyncio
import datetime
import pandas as pd
from config.config import DATA_FILE, CHAT_ID
from pymorphy3 import MorphAnalyzer

morph = MorphAnalyzer()


def add_employee(name: str, department: str, start_date: str, username: str) -> None:
    """
    Добавляет нового сотрудника в базу данных
    Args:
        name (str): Имя сотрудника
        department (str): Департамент сотрудника
        start_date (str): Дата начала работы сотрудника
        username (str): Логин сотрудника
    """
    df = pd.read_csv(DATA_FILE)
    new_employee = pd.DataFrame({
        'name': [name],
        'department': [department],
        'start_date': [start_date],
        'username': [username],
    })
    df = pd.concat([df, new_employee], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


def remove_employee(username: str, department: str) -> None:
    """
    Удаляет сотрудника из базы данных
    Args:
        username (str): Логин сотрудника для удаления
        department (str): Департамент сотрудника для подтверждения удаления
    """
    df = pd.read_csv(DATA_FILE)
    df = df[(df['username'] != username) | (df['department'] != department)]
    df.to_csv(DATA_FILE, index=False)


def read_data() -> pd.DataFrame:
    """
    Читает данные из файла базы данных
    Returns:
        pd.DataFrame: DataFrame с данными о сотрудниках
    """
    df = pd.read_csv(DATA_FILE)
    return df


async def check_anniversary():
    """
    Проверяет, есть ли сегодня день рождения у кого-то из сотрудников
    и отправляет поздравления, если есть
    """
    from handlers.send_congratulations import send_congratulations
    today = datetime.date.today()
    df = read_data()
    for index, row in df.iterrows():
        start_date = datetime.datetime.strptime(row['start_date'], '%d.%m.%Y').date()
        anniversary_date = datetime.date(today.year, start_date.month, start_date.day)
        if anniversary_date == today:
            years_in_company = today.year - start_date.year
            await send_congratulations(CHAT_ID, row['username'], row['department'], years_in_company)
            await asyncio.sleep(1)


def decline_name_parts(full_name: str) -> str:
    """
    Склоняет части имени по падежам
    Args:
        full_name (str): Полное имя
    Returns:
        str: Склоненное имя
    """
    parts = full_name.split()
    declined_parts = []
    for part in parts:
        parsed_word = morph.parse(part)[0]
        declined_part = parsed_word.inflect({'gent'}).word
        declined_parts.append(declined_part)
    return ' '.join(declined_parts)


def capitalize_name(name: str) -> str:
    """
    Переводит имя в верхний регистр
    Args:
        name (str): Имя
    Returns:
        str: Имя в верхнем регистре
    """
    return ' '.join(word.capitalize() for word in name.split())


def decline_number(number: int) -> str:
    """
    Склоняет число по падежам
    Args:
        number (int): Число
    Returns:
        str: Склоненное число
    """
    parsed_word = morph.parse('год')[0]
    declined_word = parsed_word.make_agree_with_number(number).word
    return f"{number} {declined_word}"

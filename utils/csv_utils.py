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
    Склоняет число лет по падежам
    Args:
        number (int): Количество лет
    Returns:
        str: Склоненное количество лет
    """
    if number % 10 == 1 and number % 100 != 11:
        return f"{number} год"
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return f"{number} года"
    else:
        return f"{number} лет"

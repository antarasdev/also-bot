import asyncio
import datetime
import pandas as pd
from config.config import DATA_FILE, CHAT_ID



def add_employee(name, department, start_date):
    df = pd.read_csv(DATA_FILE)
    new_employee = pd.DataFrame({
        'name': [name],
        'department': [department],
        'start_date': [start_date]
    })
    df = pd.concat([df, new_employee], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


def remove_employee(name, department):
    df = pd.read_csv(DATA_FILE)
    df = df[(df['name'] != name) | (df['department'] != department)]
    df.to_csv(DATA_FILE, index=False)


def read_data():
    df = pd.read_csv(DATA_FILE)
    return df


async def check_anniversary():
    from handlers.send_congratulations import send_congratulations
    today = datetime.date.today()
    df = read_data()
    for index, row in df.iterrows():
        start_date = datetime.datetime.strptime(row['start_date'], '%d.%m.%Y').date()
        anniversary_date = datetime.date(today.year, start_date.month, start_date.day)
        if anniversary_date == today:
            years_in_company = today.year - start_date.year
            await send_congratulations(CHAT_ID, row['name'], row['department'], years_in_company)
            await asyncio.sleep(1)


def decline_name_parts(full_name, morph):
    parts = full_name.split()
    declined_parts = []
    for part in parts:
        parsed_word = morph.parse(part)[0]
        declined_part = parsed_word.inflect({'gent'}).word
        declined_parts.append(declined_part)
    return ' '.join(declined_parts)


def capitalize_name(name):
    return ' '.join(word.capitalize() for word in name.split())


def decline_number(number, morph):
    parsed_word = morph.parse('год')[0]
    declined_word = parsed_word.make_agree_with_number(number).word
    return f"{number} {declined_word}"



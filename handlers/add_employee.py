import datetime

from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router

from config.config import CHAT_ID

from utils.states import AddEmployee
from utils.csv_utils import add_employee


router_add_employee = Router()


@router_add_employee.message(Command('add_employee'))
async def add_employee_start(message: types.Message, state: FSMContext) -> None:
    """
    Начало процесса добавления сотрудника
    Args:
        message (types.Message): Сообщение от пользователя
        state (FSMContext): Контекст состояния машины состояний
    Returns:
        None
    """
    await state.set_state(AddEmployee.name)
    await message.answer("Введите имя сотрудника:")


@router_add_employee.message(AddEmployee.name)
async def process_name(message: types.Message, state: FSMContext) -> None:
    """
    Обработка имени сотрудника
    Args:
        message (types.Message): Сообщение от пользователя
        state (FSMContext): Контекст состояния машины состояний
    Returns:
        None
    """
    await state.update_data(name=message.text)
    await state.set_state(AddEmployee.department)
    await message.answer("Введите отдел сотрудника:")


@router_add_employee.message(AddEmployee.department)
async def process_department(message: types.Message, state: FSMContext) -> None:
    """
    Обработка отдела сотрудника
    Args:
        message (types.Message): Сообщение от пользователя
        state (FSMContext): Контекст состояния машины состояний
    Returns:
        None
    """
    await state.update_data(department=message.text)
    await state.set_state(AddEmployee.username)
    await message.answer('Введите никнейм сотрудника в формате "@username"')


@router_add_employee.message(AddEmployee.username)
async def process_nickname(message: types.Message, state: FSMContext) -> None:
    """
    Обработка никнейма сотрудника
    Args:
        message (types.Message): Сообщение от пользователя
        state (FSMContext): Контекст состояния машины состояний
    Returns:
        None
    """
    await state.update_data(username=message.text)
    await state.set_state(AddEmployee.start_date)
    await message.answer("Введите дату начала работы (в формате ДД.ММ.ГГГГ):")


@router_add_employee.message(AddEmployee.start_date)
async def process_start_date(message: types.Message, state: FSMContext) -> None:
    """
    Обработка даты начала работы сотрудника
    Args:
        message (types.Message): Сообщение от пользователя
        state (FSMContext): Контекст состояния машины состояний
    Returns:
        None
    """
    await state.update_data(start_date=message.text)
    user_data = await state.get_data()
    add_employee(user_data['name'], user_data['department'], user_data['start_date'], user_data['username'])
    await message.answer("Сотрудник успешно добавлен.")
    from handlers.send_congratulations import send_congratulations
    today = datetime.date.today()
    start_date = datetime.datetime.strptime(user_data['start_date'], '%d.%m.%Y').date()
    anniversary_date = datetime.date(today.year, start_date.month, start_date.day)
    if anniversary_date <= today:
        years = today.year - start_date.year
        await send_congratulations(user_data['username'], user_data['department'], years)

    await state.clear()

from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router
from utils.states import RemoveEmployee
from utils.csv_utils import remove_employee


router_remove_employee = Router()


@router_remove_employee.message(Command('remove_employee'))
async def remove_employee_start(message: types.Message, state: FSMContext):
    await state.set_state(RemoveEmployee.name)
    await message.answer("Введите имя сотрудника, которого нужно удалить:")

@router_remove_employee.message(RemoveEmployee.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RemoveEmployee.department)
    await message.answer("Введите отдел сотрудника:")

@router_remove_employee.message(RemoveEmployee.department)
async def process_department(message: types.Message, state: FSMContext):
    await state.update_data(department=message.text)
    user_data = await state.get_data()
    remove_employee(user_data['name'], user_data['department'])
    await message.answer("Сотрудник успешно удален.")
    await state.clear()

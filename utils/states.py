from aiogram.fsm.state import State, StatesGroup


class AddEmployee(StatesGroup):
    name = State()
    department = State()
    start_date = State()
    username = State()


class RemoveEmployee(StatesGroup):
    username = State()
    department = State()

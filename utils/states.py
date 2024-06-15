from aiogram.fsm.state import State, StatesGroup


class AddEmployee(StatesGroup):
    name = State()
    department = State()
    start_date = State()


class RemoveEmployee(StatesGroup):
    name = State()
    department = State()

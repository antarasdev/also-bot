from aiogram.fsm.state import State, StatesGroup


class AddEmployee(StatesGroup):
    """
    Состояния для добавления нового сотрудника
    """
    name = State()
    department = State()
    start_date = State()
    username = State()


class RemoveEmployee(StatesGroup):
    """
    Состояния для удаления существующего сотрудника
    """
    username = State()
    department = State()

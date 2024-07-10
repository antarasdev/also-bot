from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext) -> None:
    """
    Обработчик команды /start
    Args:
        message (types.Message): Сообщение от пользователя
        state (FSMContext): Контекст состояния машины состояний
    Returns:
        None
    """
    await state.clear()
    text = 'Привет, я бот-помощник Also Production 🫶'
    await message.answer(text)

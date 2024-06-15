from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    text = 'Привет,я бот-помощник Also Production 🫶'
    await message.answer(text)

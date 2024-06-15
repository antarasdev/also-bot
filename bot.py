import asyncio
from aiogram import types, Dispatcher
from config.log_config import setup_logging
from utils import csv_utils
from config.config import API_TOKEN
from aiogram import Bot
from handlers.start import router
from handlers.add_employee import router_add_employee
from handlers.remove_employee import router_remove_employee


bot = Bot(token=API_TOKEN)


async def set_default_commands(bot):
    commands = [
        types.BotCommand(command='start', description='▶️ Запустить бота'),
        types.BotCommand(command='add_employee', description='➕ Добавить нового сотрудника'),
        types.BotCommand(command='remove_employee', description='❌ Удалить сотрудника')
    ]
    await bot.set_my_commands(commands)


async def main():
    setup_logging()
    dp = Dispatcher()
    dp.include_routers(router, router_add_employee, router_remove_employee)
    await set_default_commands(bot)
    await csv_utils.check_anniversary()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()

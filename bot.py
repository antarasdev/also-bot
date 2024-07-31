import asyncio
import logging

from config.log_config import setup_logging
from config.config import API_TOKEN
from config.scheduler import also_bot_scheduler
from aiogram import Bot, Dispatcher, types
from handlers.start import router
from handlers.add_employee import router_add_employee
from handlers.remove_employee import router_remove_employee
from handlers.send_congratulations import check_anniversary
from handlers.quotes import quotes

bot = Bot(token=API_TOKEN)


async def set_default_commands(bot: Bot) -> None:
    """
    Установка дефолтных команд бота
    Args:
        bot (Bot): Экземпляр бота
    Returns:
        None
    """
    commands = [
        types.BotCommand(command='start', description='▶️ Запустить бота'),
        types.BotCommand(command='add_employee', description='➕ Добавить нового сотрудника'),
        types.BotCommand(command='remove_employee', description='❌ Удалить сотрудника')
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    """
    Главная функция запуска бота
    Returns:
        None
    """
    setup_logging()
    dp = Dispatcher()
    dp.include_routers(router, router_add_employee, router_remove_employee, quotes)
    await set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await check_anniversary()
    scheduler = also_bot_scheduler()
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.new_event_loop()
    loop.create_task(main())
    loop.run_forever()

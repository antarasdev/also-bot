import logging


def setup_logging() -> None:
    """
    Настройка логирования для бота
    Returns:
        None
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bot.log'),  # Логирование в файл bot.log
            logging.StreamHandler()  # Логирование в консоль
        ]
    )

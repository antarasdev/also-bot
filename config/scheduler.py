from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent
from handlers.send_congratulations import check_anniversary
from handlers.quotes import send_quote
import logging


def also_bot_scheduler() -> AsyncIOScheduler:
    """
    Создает планировщик задач для проверки дней рождения сотрудников
    Returns:
        AsyncIOScheduler: Планировщик задач
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_listener(job_execution_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.add_job(send_quote, 'cron', hour=9, minute=30)
    scheduler.add_job(check_anniversary, 'cron', hour=10, minute=0)
    return scheduler


def job_execution_listener(event: JobExecutionEvent) -> None:
    """
    Слушатель событий выполнения задач
    Args:
        event (apscheduler.events.JobExecutionEvent): Событие выполнения задачи
    Returns:
        None
    """
    if event.exception:
        logging.error(f"Job crashed: {event.job_id}")
    else:
        logging.info(f"Job executed: {event.job_id}")

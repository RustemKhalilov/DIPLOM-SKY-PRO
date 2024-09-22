import os

from tasktracker.models import Task
import requests


def get_accept_the_task(task: Task):
    """
    Функция для принятия задачи
   """
    STARTED = "Принята"
    task.status = STARTED


def send_telegram_message(chat_id, message):
    """Функция отправки сообщения в телеграм"""

    params = {
        "text": message,
        "chat_id": chat_id,
    }
    requests.get(
        f"{os.getenv("TELEGRAM_URL")}{os.getenv("TELEGRAM_TOKEN")}/sendMessage",
        params=params,
    )

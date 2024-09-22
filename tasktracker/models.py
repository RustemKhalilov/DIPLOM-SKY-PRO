from datetime import datetime

from django.db import models
from config.settings import NULLABLE


class Task(models.Model):
    CREATED = "Создана"
    STARTED = "В работе"
    COMPLETED = "Завершена"
    OVERDUE = "Просрочена"
    SUSPENDED = "Приостановлена"

    STATUS_CHOICES = [
        (CREATED, "Создана"),
        (STARTED, "В работе"),
        (COMPLETED, "Завершена"),
        (SUSPENDED, "Приостановлена")
    ]

    Creator = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="Создатель задания",
        **NULLABLE
    )

    Executor = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="Исполнитель задания+",
        verbose_name="Исполнители задания",
        **NULLABLE
    )

    name = models.CharField(
        max_length=100,
        verbose_name="Название задания",
        help_text="Введите название задания",
    )

    description = models.TextField(

        verbose_name="Описание задания",
        help_text="Введите описание задания",
    )

    start_time = models.DateField(auto_now_add=True)

    end_time = models.DateField(blank=False, default=datetime.now().strftime("%d.%m.%Y"),
                                verbose_name="Срок выполнения задания",
                                help_text="Пример: 01.12.2024")

    related_task = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная с другой заданием",
        **NULLABLE,
    )

    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default=CREATED, verbose_name="Статус задания")

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return f"{self.name} Исполнитель: {self.Executor}  Статус: {self.status}"


class Message(models.Model):
    message = models.TextField(
        'Вам пришло задание'
    )


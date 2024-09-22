from django.urls import reverse
from django.test import TestCase
from tasktracker.models import Task
from users.models import User, Posts


class TasktrackerTestCase(TestCase):
    """Тестирование модели Habits"""

    def create_base_param(self):
        """Создание тестовой модели Пользователя (с авторизацией) и Привычки"""

        self.user1 = User.objects.create(
            email="user5@list.ru",
            password="shungarillamolodoy13",
            tg_nick="616492316",
        )
        self.client.force_authenticate(user=self.user1)

        self.user1.Firstname = "Рустем"

        self.user1.Surname = "Халилов"

        self.user1.Patronymic = "Вилевич"

        self.post1 = Posts.objects.create(
            Post="Начальник отдела"
        )

        self.post2 = Posts.objects.create(
            Post="Главный специалист"
        )

        self.user1.Post = self.post1

        self.user2 = User.objects.create(
            email="user6@list.ru",
            password="shungarillamolodoy15",
            tg_nick="616492316",
        )
        self.client.force_authenticate(user=self.user2)

        self.user2.Firstname = "Семенова"

        self.user2.Surname = "Екатерина"

        self.user2.Patronymic = "Федоровна"

        self.user2.Post = self.post2

        self.task1 = Task.objects.create(
            Creator=self.user1,
            Executor=self.user2,
            name="Разработка раздела",
            description="Разработать раздел ТХ для проекта Кумжинского месторождения",
            start_time="2024-09-21",
            end_time="2024-10-01",
            related_task=None,
            status="Создана"
        )

    def test_create_task(self):
        """Тестирование создания задания"""

        url = reverse("tasktracker:tasktracker_create")

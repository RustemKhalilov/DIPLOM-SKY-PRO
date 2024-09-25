from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from tasktracker.models import Task
from users.models import User, Posts
from requests_toolbelt import MultipartEncoder
import requests
import secrets


class TasktrackerTestClass(TestCase):
    """Тестирование модели Задний"""

    def setUp(self):
        pass

    def test_create_task(self):
        """Тестирование создания задания"""
        re = requests
        test_user1 = User.objects.create_user(
            email="user5@list.ru",
            password="shungarillamolodoy13",
        )
        test_user1.save()
        # Создали юзера
        test_user1.is_active = True
        # Задали параметры юзеру
        test_user1.token = secrets.token_hex(16)
        test_user1.Firstname = "Рустем"

        test_user1.Surname = "Халилов"

        test_user1.Patronymic = "Вилевич"
        # Создали должности
        test_post1 = Posts.objects.create(
            Post="Начальник отдела"
        )

        test_post2 = Posts.objects.create(
            Post="Главный специалист"
        )
        # Задали юзеру должность
        test_user1.Post = test_post1
        print(test_user1)
        # Проверка отображения пользователя
        self.assertEqual(str(test_user1), "Халилов Рустем Вилевич - Начальник отдела")

        # Создаем второго юзера
        test_user2 = User.objects.create_user(
            email="user6@list.ru",
            password="shungarillamolodoy15",
        )
        test_user2.save()

        test_user2.is_active = True
        test_user2.token = secrets.token_hex(16)
        test_user2.Firstname = "Екатерина"

        test_user2.Surname = "Семенова"

        test_user2.Patronymic = "Федоровна"

        test_user2.Post = test_post2
        # Проверка отображения пользователя
        self.assertEqual(str(test_user2), "Семенова Екатерина Федоровна - Главный специалист")
        # Создаем первую задачу
        task1 = Task.objects.create(
            Creator=test_user1,
            Executor=test_user2,
            name="Разработка раздела",
            description="Разработать раздел ТХ для проекта Кумжинского месторождения",
            end_time="2024-10-01",
            related_task=None,
            status="Создана"
        )

        # Проверка отображения задачи
        self.assertEqual(str(task1), "Разработка раздела Исполнитель: Семенова Екатерина Федоровна - Главный "
                                     "специалист  Статус: Создана")

        login = self.client.post(reverse("users:login"),
                                 data={'email': 'user5@list.ru', 'password': 'shungarillamolodoy15'},
                                 content_type='application/json')  # 'token': test_user2.token}
        print(f"ЛОГИН - {login.content}")
        token = "14a7e5f3bfca5b53be439528c0570b79"
        print(f"Токен - {token}")
        self.assertEqual(login.status_code, 200)  # Проверка что пользователь залогинился
        multipart_data = {
            "Executor": "6",
            "name": "Разработка рабочей документации",
            "description": "Разработать рабочую документацию для проекта Кумжинского месторождения",
            "end_time": "27.09.2024",
            "status": "Создана",
        }
        # Создание задание через post
        path = reverse("tasktracker:tasktracker_create")
        response = self.client.post(path, data=multipart_data, content_type="application/json")
        print(f"Создание задания -{response.content}")

        self.assertEqual(response.status_code, 302)  # Код 302 потому что от наз ожидают заполнения данных
        my_tasklist = self.client.get(reverse("tasktracker:tasktracker_list"))
        print(f"Список заданий - {my_tasklist}")



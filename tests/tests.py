from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from tasktracker.models import Task
from users.models import User, Posts
from requests_toolbelt import MultipartEncoder
from django.middleware.csrf import CsrfViewMiddleware, get_token
import requests
import secrets
import sys
from django.test import Client


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

        login = self.client.post(reverse('users:login'),
                                 data={'email': 'user6@list.ru', 'password': 'shungarillamolodoy15'},
                                 content_type='application/json')  # 'token': test_user2.token}


        # token_json = login.json()
        csrf_client = Client(enforce_csrf_checks=True)
        URL = "http://127.0.0.1:8000/users/login/"
        csrf_client.get(URL)
        csrftoken = csrf_client.cookies['csrftoken']
        # client = requests.session()
        #
        # # Retrieve the CSRF token first
        # client.get(URL)  # sets cookie
        print(f"ЛОГИН--{login.content.decode('utf-8')}")
        print(f"ТОКЕН--{csrftoken}")
        self.assertEqual(login.status_code, 200)  # Проверка что пользователь залогинился
        data = {
            "Executor": "3",
            "name": "Разработка рабочей документации",
            "description": "Разработать рабочую документацию для проекта Кумжинского месторождения",
            "end_time": "27.09.2024",
            "status": "Создана",
        }
        login_data = dict(username='user6@list.ru', password="shungarillamolodoy15", csrfmiddlewaretoken=csrftoken.value, next='/')
        r = csrf_client.post(URL, data=login_data, headers=dict(Referer=URL))
        URL = "http://127.0.0.1:8000/list/"
        my_tasklist = csrf_client.get(URL, params={"csrfmiddlewaretoken": csrftoken})
        print(f"Список заданий - {my_tasklist.content.decode('utf-8')}")
        self.assertEqual(my_tasklist.status_code, 200)  # Проверка списка заданий
        URL = "http://127.0.0.1:8000/employeesreport/"
        my_tasklist = csrf_client.get(URL, params={"csrfmiddlewaretoken": csrftoken})
        print(f"Загрузка сотрудников - {my_tasklist.content.decode('utf-8')}")
        self.assertEqual(my_tasklist.status_code, 200)  # Проверка загрузки сотрудников
        URL = "http://127.0.0.1:8000/create/"
        task_create = csrf_client.get(URL, params={"csrfmiddlewaretoken": csrftoken}, data=data)
        self.assertEqual(task_create.status_code, 200)  # Проверка загрузки сотрудников


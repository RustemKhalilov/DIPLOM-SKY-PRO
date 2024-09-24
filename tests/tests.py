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
                                 data={"email": 'user5@list.ru', "password": 'shungarillamolodoy15'})
        self.assertEqual(login.status_code, 200)  # Проверка что пользователь залогинился
        print(f"ЛОГИН - {login}")
        create_task = self.client.get(reverse("tasktracker:tasktracker_create"))
        print(f"Создание задания - {create_task}")
        self.assertEqual(create_task.status_code, 302)# Код 302 потому что от наз ожидают заполнения данных
        my_tasklist = self.client.get(reverse("tasktracker:tasktracker_list"))
        print(f"Список заданий - {my_tasklist}")
        multipart_data = {
            "Executor": "1",
            "name": "Разработка рабочей документации",
            "description": "Разработать рабочую документацию для проекта Кумжинского месторождения",
            "end_time": "2024-10-01",
            "status": "Создана"
        }

        response = self.client.post(reverse("tasktracker:tasktracker_create"), data=multipart_data,
                                     content_type='application/json')
        print(f"РЕСПОНС -{response}")
        # data = response.json()
        # self.assertEqual(data.status_code, 201)

        # Но при попытке отправить запрос такого вида
        # data = {
        #     'Creator': self.user1,
        #     'Executor': self.user2,
        #     'name': "Разработка рабочей документации",
        #     'description': "Разработать рабочую документацию для проекта Кумжинского месторождения",
        #     'start_time': "2024-09-21",
        #     'end_time': "2024-10-01",
        #     'related_task': self.task1,
        #     'status': "Создана"
        #
        # }
        # Выдает ошибку ValueError: Content-Type header is "text/html; charset=utf-8", not "application/json"
        # Я долго копл и единственное что додумался это то что на строне клиента форма, которая уходит на сервер, если псомотреть html код формы, он допольно сложный
        # и я его должен серверу и отправить обратно, как это правильно делается к сожалению нас не учили, а сам я не дошел.

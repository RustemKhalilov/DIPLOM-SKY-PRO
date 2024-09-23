from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey
from tasktracker.models import Posts

from config.settings import NULLABLE


class UserManager(BaseUserManager):
    use_in_migrations = True

    def add_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Электронный адрес должен быть указан")
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self.add_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("У суперпользователя параметр <is_staff> должен быть =True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("У суперпользователя параметр <is_superuser> должен быть=True.")

        return self.add_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()
    username = None
    Surname = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name="Фамилия",
        help_text="Укажите фамилию"
    )
    Firstname = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name="Имя",
        help_text="Укажите Имя"
    )
    Patronymic = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name="Отчество",
        help_text="Укажите отчество"
    )
    Post = ForeignKey(
        Posts,
        on_delete=models.CASCADE,
        verbose_name="Должность",
        **NULLABLE
    )

    email = models.EmailField(
        unique=True, verbose_name="Почта",
        help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        **NULLABLE,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )
    tg_nick = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name="Tg name",
        help_text="Укажите telegram-ник",
    )

    token = models.CharField(
        max_length=100,
        verbose_name='Токен',
        blank=True, null=True)

    # Задаем USERNAME_FIELD–для определения уникального идентификатора в модели User со значением email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.Surname} {self.Firstname} {self.Patronymic} - {self.Post}"

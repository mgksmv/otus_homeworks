from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager
from .validators import only_int


class User(AbstractBaseUser, PermissionsMixin):
    types = (
        ('1', 'Учитель'),
        ('2', 'Студент'),
    )

    email = models.EmailField('Почта', max_length=32, unique=True)
    first_name = models.CharField('Имя', max_length=32)
    last_name = models.CharField('Фамилия', max_length=32)
    birthday = models.DateField('День рождения', blank=True, null=True)
    photo = models.ImageField('Фотография', blank=True, null=True, default='profile_pic_default.jpg')
    phone = models.CharField('Телефон', max_length=15, validators=[only_int], blank=True, null=True)
    user_type = models.CharField('Тип пользователя', max_length=1, choices=types)

    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
    last_login = models.DateTimeField('Последний вход', auto_now_add=True)
    is_active = models.BooleanField('Активный', default=True)
    is_admin = models.BooleanField('Админ', default=False)
    is_staff = models.BooleanField('Статус персонала', default=False)
    is_superuser = models.BooleanField('Статус суперпользователя', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return f'{self.id} {self.first_name} {self.last_name}'

    def get_full_name(self):
        return str(self)

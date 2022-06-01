# Generated by Django 4.0.4 on 2022-05-24 16:59

import accounts.managers
import accounts.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=32, unique=True, verbose_name='Почта')),
                ('first_name', models.CharField(max_length=32, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=32, verbose_name='Фамилия')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('photo', models.ImageField(blank=True, default='profile_pic_default.jpg', null=True, upload_to='', verbose_name='Фотография')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, validators=[accounts.validators.only_int], verbose_name='Телефон')),
                ('user_type', models.CharField(choices=[('1', 'Учитель'), ('2', 'Студент')], max_length=1, verbose_name='Тип пользователя')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='Последний вход')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Админ')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Статус персонала')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Статус суперпользователя')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'аккаунт',
                'verbose_name_plural': 'Аккаунты',
            },
            managers=[
                ('objects', accounts.managers.UserManager()),
            ],
        ),
    ]

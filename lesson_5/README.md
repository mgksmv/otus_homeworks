Проект "Мой Блог"

Для запуска:

1. `pip install -r requirements.txt` Устанавливаем все необходимые зависимости

2. Вставляем свои данные в файл .env.template. После того, как всё ввели, удаляем часть .template с файла и комментарии внутри файла

3. `docker compose up -d` Запускаем Docker

4. `flask db init` Инициализируем Flask Migrate

5. `flask db migrate` Создаём миграции в БД

6. `flask db upgrade` Создаём все таблицы

7. `flask createsuperuser --username <ваш ник> --email <ваш email> --password <ваш пароль>` Создаём супер юзера

8. Запускаем сам проект. Либо через PyCharm, либо командой `python app.py`

9. Переходим на http://127.0.0.1:5000/ и входим в только что созданный супер юзер аккаунт

Можно и не создавать супер юзера и напрямую с формы регистрации зарегистрировать аккаунт. 

**НО** у супер юзера есть дополнительная возможность: возможность создавать теги.
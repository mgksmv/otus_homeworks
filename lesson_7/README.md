## Проект Онлайн Школа

### Чтобы запустить проект:

Добавляем SECRET_KEY и DEBUG в .env и убираем с названия часть .template

`docker compose up -d` Запускаем Docker

`docker compose exec web python manage.py migrate` Применяем миграции и создаём таблицы в БД

`docker compose exec web python manage.py createsuperuser` Создаём супер пользователя

`docker compose exec web python manage.py fill_db 20` Заполняем БД фейковыми данными (20 - количество данных для генерации. Можно указать другую цифру)

Переходим в `http://127.0.0.1:8000/admin` и вводим данные только что созданного супер пользователя

Если при переходе на сайт в консоли выходит ошибка "ValueError: Dependency on app with no migrations", то перезагружаем Docker `docker compose down` и `docker compose up -d`

`docker compose exec web pytest` - запустить тесты

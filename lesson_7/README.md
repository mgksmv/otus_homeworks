## Проект Онлайн Школа

### Чтобы запустить проект:

`pip install -r requirements` Устанавливаем все необходимые зависимости

Добавляем SECRET_KEY и DEBUG в .env и убраем с названия часть .template

`python manage.py makemigrations onlineschool` Делаем миграции

`python manage.py migrate` Применяем миграции и создаём таблицы в БД

`python manage.py createsuperuser` Создаём сюпер пользователя

`python manage.py runserver` Запускаем локальный сервер

Переходим в `http://127.0.0.1:8000/admin` и вводим данные только что созданного супер пользователя


### Краткое описание:

На данный момент имеются модели Teacher, Student, Review, Course, Schedule.
Можно создавать курс, прикреплять на него учителей, добавить описание, стоимость и т.д. Можно "организовать" курс с помощью модели Schedule, который добавляет начало и окончание курса и набранных студентов. Можно добавить студентов и преподавателей в отдельных моделях, а так же отзывы к курсу. 
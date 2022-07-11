import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from onlineschool.models import Schedule, Course, Category, Teacher

User = get_user_model()


@pytest.fixture()
def user(db):
    return User.objects.create_superuser(email='test@test.com', password='test12345')


@pytest.fixture()
def login_user(db, user, client):
    return client.login(email='test@test.com', password='test12345')


@pytest.fixture()
def user_teacher(db):
    return User.objects.create(
        email='teacher@test.com',
        first_name='Test',
        last_name='Teacher',
        password='teacher12345',
        user_type='1',
        is_active=True,
    )


@pytest.fixture()
def user_student(db):
    return User.objects.create(
        email='student@test.com',
        first_name='Test',
        last_name='Student',
        password='student12345',
        user_type='2',
        is_active=True,
    )


@pytest.fixture()
def token(user):
    return Token.objects.create(user=user)


@pytest.fixture()
def token_teacher(user_teacher):
    return Token.objects.create(user=user_teacher)


@pytest.fixture()
def token_student(user_student):
    return Token.objects.create(user=user_student)


@pytest.fixture()
def course(db, user):
    category = Category.objects.create(name='Web Development', color='#0e72ed', slug='web-development')
    teacher = Teacher.objects.get(user=user)
    course = Course.objects.create(
        category=category,
        name='Fullstack разработчик',
        duration=6,
        description='Fullstack разработчик на Python + Vue.js',
        required_knowledge='Базовые знания Python, HTML, CSS',
        after_course='После курса вы будете работать в Google (но это не точно)',
        price=50000,
        slug='fullstack-razrabotchik',
    )
    course.teachers.set([teacher])
    return course


@pytest.fixture()
def schedule(db, user, course):
    schedule = Schedule.objects.create(
        course=course,
        start_date='2022-08-01',
        end_date='2023-02-01',
        is_announced_later=False,
        slug='fullstack-razrabotchik-8-2022',
    )
    return schedule


@pytest.fixture()
def category(db, user):
    category = Category.objects.create(name='Web Development', color='#0e72ed', slug='web-development')
    return category

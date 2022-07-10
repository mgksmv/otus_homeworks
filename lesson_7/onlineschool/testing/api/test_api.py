import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from rest_framework.authtoken.models import Token

from onlineschool.api.views import CourseViewSet
from onlineschool.models import Category, Course, Teacher
from onlineschool.testing.conftest import user
from onlineschool.testing.test_course import create_course

User = get_user_model()


@pytest.fixture()
def token(user):
    return Token.objects.create(user=user)


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Tests:
    def test_get_courses_empty(self, client):
        response = client.get('/api/v1/course/')

        assert response.status_code == HTTP_200_OK
        assert response.data == []

    def test_get_courses(self, client):
        category = Category.objects.create(name='Web Development', color='#0e72ed', slug='web-development')
        Course.objects.create(
            category=category,
            name='Fullstack разработчик',
            duration=6,
            description='Fullstack разработчик на Python + Vue.js',
            required_knowledge='Базовые знания Python, HTML, CSS',
            after_course='После курса вы будете работать в Google (но это не точно)',
            price=50000,
            slug='fullstack-razrabotchik',
        )

        response = client.get('/api/v1/course/')

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1
        assert response.data == [
            {'id': 1,
             'name': 'Fullstack разработчик',
             'photo': 'http://testserver/media/course_default.png',
             'duration': 6,
             'short_description': None,
             'description': 'Fullstack разработчик на Python + Vue.js',
             'required_knowledge': 'Базовые знания Python, HTML, CSS',
             'after_course': 'После курса вы будете работать в Google (но это не точно)',
             'price': 50000,
             'slug': 'fullstack-razrabotchik',
             'category': 1,
             'teachers': []
             }
        ]

    def test_post_course_unauthorized(self, client):
        response = client.post('/api/v1/course/')

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_post_course_authorized(self, user, token):
        api_client = APIClient()
        category = Category.objects.create(name='Web Development', color='#0e72ed', slug='web-development')
        teacher = Teacher.objects.get(user=user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'name': 'Fullstack разработчик',
            'duration': 6,
            'description': 'Fullstack разработчик на Python + Vue.js',
            'required_knowledge': 'Базовые знания Python, HTML, CSS',
            'after_course': 'После курса вы будете работать в Google (но это не точно)',
            'price': 50000,
            'slug': 'fullstack-razrabotchik',
            'category': category.id,
            'teachers': [teacher.id]
        }
        response = api_client.post('/api/v1/course/', data)

        assert response.status_code == HTTP_201_CREATED

        course = Course.objects.filter(id=response.data['id']).first()

        assert Course.objects.filter(id=response.data['id']).exists() == True
        assert course.name == 'Fullstack разработчик'
        assert course.category.id == category.id
        assert teacher in course.teachers.all()

    def test_delete_course_authorized(self, client, create_course, token):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.delete(f'/api/v1/course/{create_course.id}/')

        assert response.status_code == HTTP_204_NO_CONTENT

    def test_delete_course_unauthorized(self, client, create_course):
        response = client.delete(f'/api/v1/course/{create_course.id}/')

        assert response.status_code == HTTP_401_UNAUTHORIZED

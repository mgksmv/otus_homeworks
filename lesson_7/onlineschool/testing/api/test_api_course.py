import pytest

from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from onlineschool.models import Category, Course, Teacher
from onlineschool.testing.conftest import user, token, course

PATH = '/api/v1/course/'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Tests:
    def test_get_course_list_empty(self, client):
        response = client.get(PATH)

        assert response.status_code == HTTP_200_OK
        assert response.data == []

    def test_get_course_list(self, client, course):
        response = client.get(PATH)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1
        assert response.data == [
            {
                'id': 1,
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
                'teachers': [1]
            }
        ]

    def test_post_course_unauthorized(self, client):
        response = client.post(PATH)

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
        response = api_client.post(PATH, data)

        assert response.status_code == HTTP_201_CREATED

        course = Course.objects.filter(id=response.data['id']).first()

        assert Course.objects.filter(id=response.data['id']).exists() is True
        assert course.name == 'Fullstack разработчик'
        assert course.category.id == category.id
        assert teacher in course.teachers.all()

    def test_put_course_unauthorized(self, client, user, course):
        response = client.put(f'{PATH}{course.id}/')

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_put_course_authorized(self, user, token, course):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'name': 'Fullstack разработчик на Python',
            'duration': 10,
            'description': 'Fullstack разработчик на Python + Vue.js',
            'required_knowledge': 'Базовые знания Python, HTML, CSS',
            'after_course': 'После курса вы будете работать в Google (но это не точно)',
            'price': 100000,
            'slug': 'fullstack-razrabotchik',
            'category': course.category.id,
            'teachers': [teacher.id for teacher in course.teachers.all()]
        }
        response = api_client.put(f'{PATH}{course.id}/', data)

        assert response.status_code == HTTP_200_OK

        course = Course.objects.filter(id=response.data['id']).first()

        assert course.name == 'Fullstack разработчик на Python'
        assert course.duration == 10
        assert course.price == 100000

    def test_delete_course_authorized(self, client, course, token):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.delete(f'{PATH}{course.id}/')

        assert response.status_code == HTTP_204_NO_CONTENT

    def test_delete_course_unauthorized(self, client, course):
        response = client.delete(f'{PATH}{course.id}/')

        assert response.status_code == HTTP_401_UNAUTHORIZED

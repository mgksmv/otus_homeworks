import pytest

from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from onlineschool.models import Teacher
from onlineschool.testing.conftest import user, user_teacher, token

PATH = '/api/v1/teacher/'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Tests:
    def test_get_teacher_list_empty(self, client):
        response = client.get(PATH)

        assert response.status_code == HTTP_200_OK
        assert response.data == []

    def test_get_teacher_list(self, client, user_teacher):
        response = client.get(PATH)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1
        assert response.data == [
            {
                'id': 1,
                'short_bio': '',
                'bio': '',
                'user': 1
            }
        ]

    def test_post_teacher_unauthorized(self, client):
        response = client.post(PATH)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_put_teacher_authorized(self, user_teacher, token):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'short_bio': 'Test short bio',
            'bio': 'Test bio',
            'user': 1
        }
        response = api_client.put(f'{PATH}1/', data)

        assert response.status_code == HTTP_200_OK

        teacher = Teacher.objects.filter(id=response.data['id']).first()

        assert Teacher.objects.filter(id=response.data['id']).exists() == True
        assert teacher.short_bio == 'Test short bio'
        assert teacher.bio == 'Test bio'
        assert teacher.user.id == 1

    def test_delete_teacher_authorized(self, client, user_teacher, token):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.delete(f'{PATH}{user_teacher.id}/')

        assert response.status_code == HTTP_204_NO_CONTENT

    def test_delete_teacher_unauthorized(self, client, user_teacher):
        response = client.delete(f'{PATH}{user_teacher.id}/')

        assert response.status_code == HTTP_401_UNAUTHORIZED

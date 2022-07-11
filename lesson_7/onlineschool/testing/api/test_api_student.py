import pytest

from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from onlineschool.models import Student
from onlineschool.testing.conftest import user, user_student, token

PATH = '/api/v1/student/'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Tests:
    def test_get_student_list_empty(self, client):
        response = client.get(PATH)

        assert response.status_code == HTTP_200_OK
        assert response.data == []

    def test_get_student_list(self, client, user_student):
        response = client.get(PATH)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1
        assert response.data == [
            {
                'id': 1,
                'wishlist': [],
                'user': 1
            }
        ]

    def test_post_student_unauthorized(self, client):
        response = client.post(PATH)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_put_student_authorized(self, user_student, token):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'wishlist': [],
            'user': 1
        }
        response = api_client.put(f'{PATH}1/', data)

        assert response.status_code == HTTP_200_OK

        student = Student.objects.filter(id=response.data['id']).first()

        assert Student.objects.filter(id=response.data['id']).exists() == True
        assert student.user.id == 1

    def test_delete_student_authorized(self, client, user_student, token):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.delete(f'{PATH}{user_student.id}/')

        assert response.status_code == HTTP_204_NO_CONTENT

    def test_delete_student_unauthorized(self, client, user_student):
        response = client.delete(f'{PATH}{user_student.id}/')

        assert response.status_code == HTTP_401_UNAUTHORIZED

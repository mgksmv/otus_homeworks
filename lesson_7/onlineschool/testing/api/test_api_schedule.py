import pytest

from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from onlineschool.models import Schedule
from onlineschool.testing.conftest import user, token, course, schedule

PATH = '/api/v1/schedule/'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Tests:
    def test_get_schedule_list_empty(self, client):
        response = client.get(PATH)

        assert response.status_code == HTTP_200_OK
        assert response.data == []

    def test_get_schedule_list(self, client, schedule):
        response = client.get(PATH)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1
        assert response.data == [
            {
                'id': 1,
                'start_date': '2022-08-01',
                'end_date': '2023-02-01',
                'is_announced_later': False,
                'slug': 'fullstack-razrabotchik-8-2022',
                'course': 1,
                'students': []
            }
        ]

    def test_post_schedule_unauthorized(self, client):
        response = client.post(PATH)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_post_schedule_authorized(self, user, token, course):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'course': course.id,
            'start_date': '2022-10-01',
            'end_date': '2023-04-01',
            'is_announced_later': False,
            'slug': 'fullstack-razrabotchik-8-2022',
        }
        response = api_client.post(PATH, data)

        assert response.status_code == HTTP_201_CREATED

        schedule = Schedule.objects.filter(id=response.data['id']).first()

        assert Schedule.objects.filter(id=response.data['id']).exists() == True
        assert schedule.course == course

    def test_delete_schedule_authorized(self, client, schedule, token):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.delete(f'{PATH}{schedule.id}/')

        assert response.status_code == HTTP_204_NO_CONTENT

    def test_delete_schedule_unauthorized(self, client, schedule):
        response = client.delete(f'{PATH}{schedule.id}/')

        assert response.status_code == HTTP_401_UNAUTHORIZED

import pytest

from ..models import Schedule
from .test_course import create_course


@pytest.fixture()
def create_schedule(db, user, create_course):
    schedule = Schedule.objects.create(
        course=create_course,
        start_date='2022-08-01',
        end_date='2023-02-01',
        is_announced_later=False,
        slug='fullstack-razrabotchik-8-2022',
    )
    return schedule


@pytest.mark.django_db
class Tests:
    def test_create_schedule_page(self, client, login_user):
        response = client.get('/courses/create-group/')
        assert response.status_code == 200

    def test_create_schedule_page_unauthorized(self, client):
        response = client.get('/courses/create-group/')
        assert response.status_code == 302

    def test_create_schedule(self, client, login_user, create_course):
        response = client.post('/courses/create-group/', {
            'course': create_course.id,
            'start_date': '2022-08-01',
            'end_date': '2023-02-01',
            'is_announced_later': False,
            'slug': 'fullstack-razrabotchik-8-2022',
        })
        assert response.status_code == 302
        assert Schedule.objects.all().count() == 1

    def test_update_schedule(self, client, login_user, create_course, create_schedule):
        response = client.post('/courses/update-group/fullstack-razrabotchik-8-2022/', {
            'course': create_course.id,
            'start_date': '2022-10-01',
            'end_date': '2023-04-01',
            'is_announced_later': True,
            'slug': 'fullstack-razrabotchik-8-2022',
        })
        assert response.status_code == 302
        assert Schedule.objects.get(slug='fullstack-razrabotchik-8-2022').is_announced_later is True
        assert Schedule.objects.all().count() == 1

    def test_schedule_list_view(self, client, login_user, create_schedule):
        response = client.get('/courses/schedule/')
        assert response.status_code == 200
        assert 'Расписание курсов'.encode('utf-8') in response.content
        assert 'Fullstack разработчик'.encode('utf-8') in response.content

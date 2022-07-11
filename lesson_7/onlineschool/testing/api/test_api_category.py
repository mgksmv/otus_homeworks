import pytest

from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from onlineschool.models import Category
from onlineschool.testing.conftest import user, token, category

PATH = '/api/v1/category/'


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Tests:
    def test_get_category_list_empty(self, client):
        response = client.get(PATH)

        assert response.status_code == HTTP_200_OK
        assert response.data == []

    def test_get_category_list(self, client, category):
        response = client.get(PATH)

        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1
        assert response.data == [
            {
                'id': 1,
                'name': 'Web Development',
                'color': '#0e72ed',
                'slug': 'web-development'
            }
        ]

    def test_post_category_unauthorized(self, client):
        response = client.post(PATH)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_post_category_authorized(self, user, token):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'name': 'Web Development',
            'color': '#0e72ed',
            'slug': 'web-development'
        }
        response = api_client.post(PATH, data)

        assert response.status_code == HTTP_201_CREATED

        category = Category.objects.filter(id=response.data['id']).first()

        assert Category.objects.filter(id=response.data['id']).exists() is True
        assert category.name == 'Web Development'
        assert category.color == '#0e72ed'
        assert category.slug == 'web-development'

    def test_put_category_unauthorized(self, client, user, category):
        response = client.put(f'{PATH}{category.id}/')

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_put_category_authorized(self, user, token, category):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            'name': 'WEB',
            'color': '#000',
            'slug': 'web'
        }
        response = api_client.put(f'{PATH}{category.id}/', data)

        assert response.status_code == HTTP_200_OK

        category_ = Category.objects.filter(id=response.data['id']).first()

        assert category_.name == 'WEB'
        assert category_.color == '#000'
        assert category_.slug == 'web'

    def test_delete_category_authorized(self, client, category, token):
        api_client = APIClient()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.delete(f'{PATH}{category.id}/')

        assert response.status_code == HTTP_204_NO_CONTENT

    def test_delete_category_unauthorized(self, client, category):
        response = client.delete(f'{PATH}{category.id}/')

        assert response.status_code == HTTP_401_UNAUTHORIZED

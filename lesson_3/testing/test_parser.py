from unittest.mock import patch, Mock
from pytest import fixture
from bs4 import BeautifulSoup
from lesson_3.parser import YcombinatorParser


class Response:
    @property
    def text(self):
        with open('website.txt', 'r') as file:
            file_text = file.read()
        return file_text


@fixture
def parser() -> YcombinatorParser:
    return YcombinatorParser(1)


def mock_get_response(*args, **kwargs):
    return Response()


@patch.object(YcombinatorParser, 'get_response', mock_get_response)
class TestParser:
    def test_get_soup(self, parser):
        soup = parser.get_soup()
        assert isinstance(soup, BeautifulSoup) is True

    def test_get_links(self, parser):
        links = parser.get_links()
        assert links is not None

    def test_one_link(self, parser):
        link = parser.get_links()[0]
        assert link.startswith('https') is True

    def test_get_inner_links(self, parser):
        inner_links = parser.get_inner_links(parser.get_links())
        assert inner_links is not None

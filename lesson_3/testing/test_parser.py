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


class TestParser:
    @patch.object(YcombinatorParser, 'get_response')
    def test_get_soup(self, mock_get_response, parser):
        mock_get_response.return_value = Response()
        soup = parser.get_soup()
        assert isinstance(soup, BeautifulSoup) is True

    @patch.object(YcombinatorParser, 'get_response')
    def test_get_links(self, mock_get_response, parser):
        mock_get_response.return_value = Response()
        links = parser.get_links()
        assert links is not None

    @patch.object(YcombinatorParser, 'get_response')
    def test_one_link(self, mock_get_response, parser):
        mock_get_response.return_value = Response()
        link = parser.get_links()[0]
        assert link.startswith('https') is True

    @patch.object(YcombinatorParser, 'get_response')
    def test_get_inner_links(self, mock_get_response, parser):
        mock_get_response.return_value = Response()
        inner_links = parser.get_inner_links(parser.get_links())
        assert inner_links is not None

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


@fixture
@patch.object(YcombinatorParser, 'get_response')
def mocked_parser(mock_get_response, parser) -> YcombinatorParser:
    mock_get_response.return_value = Response()
    return parser


class TestParser:
    def test_get_soup(self, mocked_parser):
        soup = mocked_parser.get_soup()
        assert isinstance(soup, BeautifulSoup) is True

    def test_get_links(self, mocked_parser):
        links = mocked_parser.get_links()
        assert links is not None

    def test_one_link(self, mocked_parser):
        link = mocked_parser.get_links()[0]
        assert link.startswith('https') is True

    def test_get_inner_links(self, mocked_parser):
        inner_links = mocked_parser.get_inner_links(mocked_parser.get_links())
        assert inner_links is not None

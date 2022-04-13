from pytest import fixture
from bs4 import BeautifulSoup
from lesson_3.parser import YcombinatorParser


@fixture
def parser() -> YcombinatorParser:
    return YcombinatorParser(1)


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

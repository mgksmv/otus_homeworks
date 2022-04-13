import random
from string import ascii_lowercase
from pytest import fixture
from lesson_3.loto import Player, Card, Bag

letters = random.choices(ascii_lowercase, k=6)
random_name = ''.join(letters)


@fixture
def card() -> Card:
    return Card()


@fixture
def player(card) -> Player:
    return Player(card, random_name)


@fixture
def bag() -> Bag:
    return Bag()


class TestCard:
    def test_init(self, card):
        assert card.numbers is None
        assert isinstance(card, Card)

    def test_generate_cars(self, card):
        generated_numbers = card.generate_card()
        card.numbers = generated_numbers
        assert len(card.numbers) > 0


class TestPlayer:
    def test_init(self, player):
        assert player.name == random_name


class TestBag:
    def test_init(self, bag):
        assert len(bag.barrels) == 90

    def test_get_new_barrel(self, bag):
        new_barrel = bag.get_new_barrel()
        assert new_barrel not in bag.barrels

import builtins
import random
from string import ascii_lowercase
from unittest import TestCase, mock
from pytest import fixture
from lesson_2.main import Game, Player, Card

letters = random.choices(ascii_lowercase, k=8)
random_name = ''.join(letters)


@fixture
def player() -> Player:
    card = Card()
    player = Player(card, random_name)
    return player


class TestPlayer:
    def test_init(self):
        name = 'goose'
        card = Card()
        player = Player(card, name)
        assert player.name == name



# class TestLotoGame(TestCase):
#
#     def setUp(self) -> None:
#         self.game = Game()
#
#     def test_human_vs_ai(self):
#         mode = self.game.human_vs_ai()
#         with mock.patch.object(builtins, 'input', lambda _: 'y'):
#             assert

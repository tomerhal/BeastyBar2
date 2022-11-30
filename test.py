import copy
import random

from board import Player, Game
from graphics import *
from testGraphics import TestGraphics
from cards import *
from testCards import *

first_deck = [Lion(), Hippo(), Crocodile(), Snake(), Giraffe(), Zebra(), Seal(), Chameleon(), Monkey(), Kangaroo(), Parrot(), Skunk()]
second_deck = [Rhino(), Bear(), Tiger(), Cheetah(), Llama(), Porcupine(), Ostrich(), Penguin(), Dog(), Peacock(), Vulture(), Bat()]
third_deck = [Elephant(), Camel(), Buffalo(), Eagle(), Okapi(), Sloth(), Panda(), Coyote(), Weasel(), Gazelle(), Flamingo(), Armadillo()]
third_deck13 = [Elephant(), Camel(), Buffalo(), Eagle(), Okapi(), Sloth(), Panda(), Coyote(), Weasel(), Gazelle(), Flamingo(), Armadillo(), TasmanianDevil()]

test_deck = [Bat(), Rock(), Plant()]
test_second_deck = [Plant(), Rock(), Bat()]


def test_decks():
    testPlayer1 = Player('test0', Colors.White, test_deck, CMDGraphics)
    testPlayer2 = Player('test0', Colors.LightBlue, test_second_deck, CMDGraphics)
    players = [testPlayer1, testPlayer2]
    Game(players, players[0].deck_len)


def real_game_decks():
    testPlayer1 = Player('Nir1', Colors.Blue, copy.deepcopy(first_deck), CMDGraphics, random.randint(0, 100))
    testPlayer2 = Player('Nir2', Colors.Green, copy.deepcopy(second_deck), CMDGraphics, random.randint(0, 100))
    testPlayer3 = Player('Nir3', Colors.Red, copy.deepcopy(third_deck), CMDGraphics, random.randint(0, 100))
    testPlayer4 = Player('Nir4', Colors.Yellow, copy.deepcopy(second_deck), CMDGraphics, random.randint(0, 100))
    players = [testPlayer1, testPlayer2, testPlayer3, testPlayer4]
    Game(players, players[0].deck_len)


def auto_testers():
    tester1 = Player('tester1', Colors.Blue, copy.deepcopy(first_deck), TestGraphics, random.randint(0, 100))
    tester2 = Player('tester2', Colors.Green, copy.deepcopy(second_deck), TestGraphics, random.randint(0, 100))
    tester3 = Player('tester3', Colors.Red, copy.deepcopy(third_deck), TestGraphics, random.randint(0, 100))
    tester4 = Player('tester4', Colors.Yellow, copy.deepcopy(third_deck), TestGraphics, random.randint(0, 100))
    players = [tester1, tester2, tester3, tester4]
    Game(players, players[0].deck_len)


def auto_testing_100():
    for i in range(1000):
        auto_testers()


def auto_testers_with_seeds(s1, s2, s3, s4):
    tester1 = Player('tester1', Colors.Blue, copy.deepcopy(first_deck), TestGraphics, s1)
    tester2 = Player('tester2', Colors.Green, copy.deepcopy(second_deck), TestGraphics, s2)
    tester3 = Player('tester3', Colors.Red, copy.deepcopy(third_deck), TestGraphics, s3)
    tester4 = Player('tester4', Colors.Yellow, copy.deepcopy(third_deck), TestGraphics, s4)
    players = [tester1, tester2, tester3, tester4]
    Game(players, players[0].deck_len)


if __name__ == "__main__":
    # auto_testers()
    # auto_testing_100()
    # auto_testers_with_seeds(97, 9, 77, 18)
    real_game_decks()
    # test_decks()

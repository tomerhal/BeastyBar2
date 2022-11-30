import copy

from board import Board
from card import Card, CardTypes


class Dog(Card):  # Done

    def __init__(self):
        super().__init__(4, "Dog", 2, False, False, CardTypes.Undefined, 2)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        jostling_copy = copy.deepcopy(game_state.jostling_cards)
        jostling_copy.sort(key=Card.compare)
        new_indexes = []
        for card in jostling_copy:
            new_indexes.append(card.index)
        return [[Board.reorder, new_indexes]]

import copy

from board import Board
from card import Card, CardTypes


class Snake(Card):  # Done

    def __init__(self):
        super().__init__(9, "Snake", 2, False, False, CardTypes.Undefined, 1)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        jostling_copy = copy.deepcopy(game_state.jostling_cards)
        print(jostling_copy)
        jostling_copy.sort(key=Card.compare, reverse=True)
        new_indexes = []
        for card in jostling_copy:
            new_indexes.append(card.index)
        # print("new indexes", new_indexes)
        return [[Board.reorder, new_indexes]]

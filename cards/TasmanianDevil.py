import random

from board import Board
from card import Card, CardTypes


class TasmanianDevil(Card):  # Done

    def __init__(self):
        super().__init__(0, "Tasmanian Devil", 2, False, False, CardTypes.Undefined, 3)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        indexes = []
        for card in game_state.jostling_cards:
            if card.id != self.id:
                indexes.append(card.index)

        random.shuffle(indexes)
        indexes.insert(0, self.index)

        return [[Board.reorder, indexes]]

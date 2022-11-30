from board import Board
from card import Card, CardTypes


class Seal(Card):  # Done

    def __init__(self):
        super().__init__(6, "Seal", 2, False, False, CardTypes.Undefined, 1)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        new_indexes = []
        for card in game_state.jostling_cards:
            new_indexes.insert(0, card.index)
        return [[Board.reorder, new_indexes]]

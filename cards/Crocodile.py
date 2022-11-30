from board import Board
from card import Card, CardTypes


class Crocodile(Card):  # Done

    def __init__(self):
        super().__init__(10, "Crocodile", 3, True, False, CardTypes.Big_Bruiser, 1)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        return [[Board.advance_to_front, self.id, True]]

    def stopping_condition(self, card):
        return card.strength >= self.strength

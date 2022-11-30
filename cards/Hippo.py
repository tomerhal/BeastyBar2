from board import Board
from card import Card, CardTypes


class Hippo(Card):  # Done

    def __init__(self):
        super().__init__(11, "Hippo", 2, True, False, CardTypes.Trampler, 1)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        return [[Board.advance_to_front, self.id]]

    def stopping_condition(self, card):
        return card.strength >= self.strength

from board import Board
from card import Card, CardTypes


class Giraffe(Card):  # Done

    def __init__(self,):
        super().__init__(8, "Giraffe", 3, True, False, CardTypes.Undefined, 1)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        return [[Board.advance_by_id, self.id]]

    def stopping_condition(self, card):
        return card.strength >= self.strength

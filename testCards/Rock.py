from board import Board
from card import Card, CardTypes


class Rock(Card):  # Done

    def __init__(self):
        super().__init__(0, "Rock", 4, False, False, CardTypes.Undefined, 0)

    def place(self, game_state):
        return [Board.join]
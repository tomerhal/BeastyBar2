from board import Board
from card import Card, CardTypes


class Plant(Card):  # Done

    def __init__(self):
        super().__init__(0, "Plant", 4, False, False, CardTypes.Undefined, 0)

    def place(self, game_state):
        return [Board.join]
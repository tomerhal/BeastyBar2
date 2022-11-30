from board import Board
from card import Card, CardTypes


class Flamingo(Card):  # Done

    def __init__(self):
        super().__init__(2, "Flamingo", 4, False, False, CardTypes.Undefined, 3)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        if self.index > 1:
            return [[Board.switch_2_cards, self.index - 2, self.index - 1], [Board.overtake, self.id]]
        return []

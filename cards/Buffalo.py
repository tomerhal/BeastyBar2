from board import Board
from card import Card, CardTypes


class Buffalo(Card):  # Done

    def __init__(self):
        super().__init__(10, "Buffalo", 3, True, False, CardTypes.Big_Bruiser, 3)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        return [[Board.advance_by_id, self.id, True]]

    def stopping_condition(self, card):
        return self.index == 0 or card.strength >= self.strength or card.card_type == CardTypes.Shield

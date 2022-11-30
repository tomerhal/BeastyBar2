from board import Board
from card import Card, CardTypes


class Vulture(Card):  # Done

    def __init__(self):
        super().__init__(2, "Vulture", 2, False, False, CardTypes.Doppelganger, 2)

    def place(self, game_state):
        return [Board.join_back_ally]

    def ability(self, game_state):
        if len(game_state.trash) > 0:
            card_to_rev = game_state.trash[-1]
            if card_to_rev.name == self.name:
                return [[Board.enter_from_back_ally], [Board.revive_enter]]
            else:
                return [[Board.revive]]
        else:
            return []

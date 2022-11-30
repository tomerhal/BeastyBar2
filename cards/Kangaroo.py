from board import Board
from card import Card, CardTypes


class Kangaroo(Card):

    def __init__(self):
        super().__init__(3, "Kangaroo", 4, False, False, CardTypes.Undefined, 1)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        if game_state.cards_in_line > 1:
            if game_state.cards_in_line > 2:
                spaces_to_jump = self.player.graphics_engine.get_kangaroo_input()
                return [[Board.overtake, self.id, spaces_to_jump]]
            else:
                return [[Board.overtake, self.id]]

        return []

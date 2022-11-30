from board import Board
from card import Card, CardTypes


class Armadillo(Card):

    def __init__(self):
        super().__init__(1, "Armadillo", 4, False, False, CardTypes.Little_Bully, 3)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        strength = self.player.graphics_engine.get_strength(game_state)
        ids_to_skip = []
        if strength == self.strength:
            ids_to_skip.append(self.id)
        return [[Board.jump_to_front, self.id], [Board.kick_all_by_strength, strength, ids_to_skip]]

from board import Board
from card import Card, CardTypes


class Coyote(Card):

    def __init__(self):
        super().__init__(5, "Coyote", 4, False, False, CardTypes.Little_Bully, 3)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        card = self.player.graphics_engine.get_card(game_state)
        return [[Board.jump_to_back, card.id], [Board.activate_ability, card.ability(game_state)]]

import copy

from board import Board
from card import Card, CardTypes
from graphics import Colors


class Chameleon(Card):

    def __init__(self):
        super().__init__(5, "Chameleon", 3, False, False, CardTypes.Undefined, 1)

    def place(self, game_state):
        activate_power = False
        for card in game_state.jostling_cards:
            if card.name != self.name:
                activate_power = True
                break

        if activate_power:
            card_index = self.player.graphics_engine.get_chameleon_input(game_state)
            card = copy.deepcopy(game_state.jostling_area[card_index])
            card.color = Colors.Grey
            self.imitate(card)
        return [Board.join, -1, self.imitating]

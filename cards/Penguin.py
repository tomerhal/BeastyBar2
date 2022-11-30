import copy

from board import Board
from card import Card, CardTypes
from graphics import Colors


class Penguin(Card):

    def __init__(self):
        super().__init__(5, "Penguin", 3, False, False, CardTypes.Doppelganger, 2)

    def place(self, game_state):
        if game_state.cards_in_line > 0 and len(self.player.hand) > 1:
            card_index = self.player.graphics_engine.get_card_from_hand(self.player.hand)
            card = copy.deepcopy(self.player.hand[card_index])
            card.color = Colors.Grey
            self.imitate(card)
            if card.name == 'Vulture':
                return [Board.join_back_ally]
        return [Board.join, -1, self.imitating]

from board import Board
from card import Card, CardTypes


class Parrot(Card):

    def __init__(self):
        super().__init__(2, "Parrot", 4, False, False, CardTypes.Little_Bully, 1)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):

        if game_state.cards_in_line == 2:
            card_to_kick = game_state.jostling_cards[0]
            return [[Board.kick_by_id, card_to_kick.id]]

        elif game_state.cards_in_line > 1:
            card_to_kick = self.player.graphics_engine.get_card(game_state)
            return [[Board.kick_by_id, card_to_kick.id]]

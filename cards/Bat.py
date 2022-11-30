from board import Board
from card import Card, CardTypes


class Bat(Card):

    def __init__(self):
        super().__init__(1, "Bat", 4, False, True, CardTypes.Little_Bully, 2)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        if game_state.cards_in_line == 2:
            card_id = game_state.jostling_cards[0].id
        else:
            card_id = self.player.graphics_engine.get_bat_input(game_state)
        return [[Board.replace, card_id, self.id]]

    def permanent_ability(self, game_state):
        print("bat id: " + self.id)
        return [[Board.kick_by_id, self.id]]

    def permanent_ability_positional_trigger(self):
        return self.index == 0

from board import Board
from card import Card, CardTypes


class Parrot(Card):

    def __init__(self,next_ability_input=None):
        super().__init__(2, "Parrot", 4, False, False, CardTypes.Little_Bully, 1)
        self.next_ability_input=next_ability_input

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        if self.next_ability_input is None:
            return []
        if game_state.cards_in_line == 2:
            card_to_kick = game_state.jostling_cards[0]
            return [[Board.kick_by_id, card_to_kick.id]]

        elif game_state.cards_in_line > 1:
            #card_to_kick = self.player.graphics_engine.get_card(game_state)
            card_to_kick = game_state.get_card_by_name(self.next_ability_input)
            return [[Board.kick_by_id, card_to_kick.id]]

    def legal_actions(self,cards_in_line,hand):
        actions = [self.name]
        if len(cards_in_line) > 1:
            for card in cards_in_line:
                if (self.name + " " + card.name) not in actions:
                    actions.append(self.name + " " + card.name)
        return actions

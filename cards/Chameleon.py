import copy

from board import Board
from card import Card, CardTypes
from graphics import Colors


class Chameleon(Card):

    def __init__(self,next_ability_input=None):
        super().__init__(5, "Chameleon", 3, False, False, CardTypes.Undefined, 1)
        self.next_ability_input=next_ability_input

    def place(self, game_state):
        activate_power = False
        for card in game_state.jostling_cards:
            if card.name != self.name:
                activate_power = True
                break
        print(self.next_ability_input)
        if activate_power and self.next_ability_input is not None:
            #card_index = self.player.graphics_engine.get_chameleon_input(game_state) #game.getidxbyname(action)
            card_index = game_state.get_card_by_name(self.next_ability_input).index
            card = copy.deepcopy(game_state.jostling_area[card_index])
            card.color = Colors.Grey
            self.imitate(card)
        return [Board.join, -1, self.imitating]

    def legal_actions(self,cards_in_line,hand):
        actions = [self.name]
        if len(cards_in_line) > 1:
            for card in cards_in_line:
                if (self.name + " " + card.name) not in actions and card.name not in ["Chameleon","Parrot","Kangaroo"]:
                    actions.append(self.name + " " + card.name)
        return actions

from board import Board
from card import Card, CardTypes


class Skunk(Card):  # Done

    def __init__(self):
        super().__init__(1, "Skunk", 4, False, False, CardTypes.Little_Bully, 1)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        highest_strength = -1
        second_highest_strength = -1
        for card in game_state.jostling_cards:
            strength = card.strength
            if strength > highest_strength and card.name != self.name:
                second_highest_strength = highest_strength
                highest_strength = strength
            elif highest_strength > strength > second_highest_strength and card.name != self.name:
                second_highest_strength = strength

        actions = []
        if highest_strength >= 0:
            actions.append([Board.kick_all_by_strength, highest_strength])
        if second_highest_strength >= 0:
            actions.append([Board.kick_all_by_strength, second_highest_strength])
        return actions

from board import Board
from card import Card, CardTypes


class Bear(Card):  # Done

    def __init__(self):
        super().__init__(11, "Bear", 2, False, False, CardTypes.Big_Bruiser, 2)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        actions = []
        lowes_strength = 13
        second_lowes_strength = 13
        for card in game_state.jostling_cards:
            if card.id != self.id:
                strength = card.strength
                if strength < lowes_strength:
                    second_lowes_strength = lowes_strength
                    lowes_strength = strength
                elif lowes_strength < strength < second_lowes_strength:
                    second_lowes_strength = strength

        for card in game_state.jostling_cards:
            if card.strength <= second_lowes_strength and card.id != self.id:
                actions.append([Board.jump_to_back, card.id])

        return actions

from board import Board
from card import Card, CardTypes


class Llama(Card):  # Done

    def __init__(self):
        super().__init__(8, "Llama", 4, True, False, CardTypes.Undefined, 2)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        actions = []
        next_card = game_state.jostling_cards[self.index - 1]
        if self.index > 0 and not self.stopping_condition(next_card):
            actions = [[Board.jump_to_back, next_card.id]]
            print(next_card.id)
        return actions

    def stopping_condition(self, card):
        return card.strength >= self.strength

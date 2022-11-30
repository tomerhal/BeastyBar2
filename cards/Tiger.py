from board import Board
from card import Card, CardTypes


class Tiger(Card):  # Done

    def __init__(self):
        super().__init__(10, "Tiger", 3, True, False, CardTypes.Big_Bruiser, 2)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        actions = []
        if self.index == 1:
            actions = [[Board.jump_by_index, 1, 0]]
        elif self.index > 1 and not self.stopping_condition(game_state.jostling_cards[self.index - 2]):
            actions = [[Board.replace, game_state.jostling_cards[self.index - 2].id, self.id]]

        return actions

    def recurring_ability(self, game_state):
        return [[Board.advance_by_index, self.index, True]]

    def stopping_condition(self, card):
        return card.strength >= self.strength or card.card_type == CardTypes.Shield

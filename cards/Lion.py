from board import Board
from card import Card, CardTypes


class Lion(Card):  # Done

    def __init__(self):
        super().__init__(12, "Lion", 2, False, False, CardTypes.Undefined, 1)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        actions = []
        other_lion = False

        for i, card in enumerate(game_state.jostling_cards):
            if card.name == "Lion" and card.color != self.color:
                actions.append([Board.kick_last])
                other_lion = True

        if not other_lion:
            actions.append([Board.jump_to_front, self.id])
        actions.append([Board.kick_all_by_name, 'Monkey'])

        return actions

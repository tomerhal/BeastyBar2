from board import Board
from card import Card, CardTypes


class Monkey(Card):  # Done

    def __init__(self):
        super().__init__(4, "Monkey", 3, False, False, CardTypes.Undefined, 1)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        actions = []
        for card in game_state.jostling_cards:
            if card.id != self.id and card.name == self.name:
                actions.append([Board.jump_to_front, card.id])

        if len(actions):
            actions += [[Board.jump_to_front, self.id], [Board.kick_all_by_type, CardTypes.Trampler], [Board.kick_all_by_type, CardTypes.Big_Bruiser]]

        return actions

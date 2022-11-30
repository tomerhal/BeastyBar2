from board import Board
from card import Card, CardTypes


class Sloth(Card):

    def __init__(self):
        super().__init__(7, "Sloth", 2, False, True, CardTypes.Shield, 3)
        self.cards_snapshot = []

    def place(self, game_state):
        self.cards_snapshot = []
        for card in game_state.jostling_cards:
            self.cards_snapshot.append(card.id)
        index = -1
        if game_state.cards_in_line > 0:
            index = self.player.graphics_engine.get_sloth_input(game_state)
        return [Board.join, index]

    def permanent_ability_interactional_trigger(self, card):
        print('Sloth was activated')
        print(card.id, self.cards_snapshot)
        return card.id in self.cards_snapshot

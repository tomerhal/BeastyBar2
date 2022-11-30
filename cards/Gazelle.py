from board import Board
from card import Card, CardTypes


class Gazelle(Card):  # Done

    def __init__(self):
        super().__init__(3, "Gazelle", 2, False, True, CardTypes.Undefined, 3)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def permanent_ability_interactional_trigger(self, card):
        return card.card_type == CardTypes.Big_Bruiser

    def permanent_ability(self, card):
        return [[Board.enter_by_id, self.id]]

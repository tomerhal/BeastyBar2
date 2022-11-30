from board import Board
from card import Card, CardTypes


class Okapi(Card):  # Done

    def __init__(self):
        super().__init__(8, "Okapi", 3, True, True, CardTypes.Shield, 3)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        return [[Board.advance_by_id, self.id]]

    def stopping_condition(self, card):
        return card.strength >= self.strength

    def permanent_ability_interactional_trigger(self, card):
        return card.card_type == CardTypes.Big_Bruiser or card.card_type == CardTypes.Trampler

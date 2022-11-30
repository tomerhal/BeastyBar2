from board import Board
from card import Card, CardTypes


class Porcupine(Card):  # Done

    def __init__(self):
        super().__init__(7, "Porcupine", 4, False, True, CardTypes.Shield, 2)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def permanent_ability(self, card):
        return [[Board.kick_by_id, card.id]]

    def permanent_ability_interactional_trigger(self, card):
        return card.card_type == CardTypes.Big_Bruiser

from board import Board
from card import Card, CardTypes


class Rhino(Card):

    def __init__(self):
        super().__init__(12, "Rhino", 3, False, False, CardTypes.Big_Bruiser, 2)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        max_strength = -1
        card_id = None
        multiple_cards = False
        for card in game_state.jostling_cards:
            if card.id != self.id:
                if card.strength > max_strength:
                    max_strength = card.strength
                    card_id = card.id
                    multiple_cards = False

                elif card.strength == max_strength:
                    multiple_cards = True

        if multiple_cards:
            input_card_id = self.player.graphics_engine.get_all_cards_of_strength_input(game_state, max_strength)
            return [[Board.replace, input_card_id, self.id]]
        else:
            return [[Board.replace, card_id, self.id]]

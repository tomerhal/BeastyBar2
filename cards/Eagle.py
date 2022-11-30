from board import Board
from card import Card, CardTypes


class Eagle(Card):  # Done

    def __init__(self):
        super().__init__(9, "Eagle", 2, False, False, CardTypes.Big_Bruiser, 3)

    def place(self, game_state):
        return [Board.join]

    def ability(self, game_state):
        if game_state.card_in_sky:
            return [[Board.kick_by_id, self.id]]
        else:
            return [[Board.fly, self.id]]

    def full_jostling_area_ability(self, game_state):
        min_strength = 13
        dive_index = 0
        for card in game_state.jostling_cards:
            if card.strength < min_strength:
                min_strength = card.strength
                dive_index = card.index
                print(min_strength, dive_index)

        if min_strength < 9:
            print("diving to", dive_index)
            return [[Board.sweep_down, dive_index]]
        else:
            return [[Board.kick_from_sky]]
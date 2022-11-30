from board import Board
from card import Card, CardTypes


class Elephant(Card):  # Done

    def __init__(self):
        super().__init__(12, "Elephant", 3, False, False, CardTypes.Undefined, 3)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        strengths_sum = 0
        spaces_to_jump = 0
        for i, card in enumerate(game_state.jostling_cards):
            if card.id != self.id:
                strengths_sum += card.strength
                if strengths_sum <= 12:
                    spaces_to_jump += 1
                else:
                    break
        return [[Board.overtake, self.id, spaces_to_jump]]

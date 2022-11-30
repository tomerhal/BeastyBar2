from board import Board
from card import Card, CardTypes


class Ostrich(Card):

    def __init__(self):
        super().__init__(6, "Ostrich", 3, False, False, CardTypes.Undefined, 2)

    def place(self, game_state):
        return [Board.join, -1, game_state.cards_in_line != 0]

    def ability(self, game_state):
        if game_state.cards_in_line > 1:
            even = self.player.graphics_engine.get_ostrich_input()
            jump_index_offset = 0
            for i in reversed(range(game_state.cards_in_line)):
                card = game_state.jostling_cards[i]
                if card.id != self.id:
                    print(i, card.strength, even)
                    if card.strength % 2 != even:
                        print('jumping over a card')
                        jump_index_offset += 1
                    else:
                        print('stop jumping', jump_index_offset)
                        return [[Board.overtake, self.id, jump_index_offset]]
            else:
                return [[Board.jump_to_front, self.id]]
        return []

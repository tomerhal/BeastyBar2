from board import Board
from card import Card, CardTypes


class Panda(Card):

    def __init__(self):
        super().__init__(6, "Zen-Panda", 4, False, False, CardTypes.Little_Bully, 3)

    def place(self, game_state):
        cards_in_line = game_state.cards_in_line
        if cards_in_line < 2:
            return [Board.join, -1, False]
        if cards_in_line == 2:
            return [Board.join, 1, False]
        else:
            index = self.player.graphics_engine.get_panda_input(game_state)
            return [Board.join, index]

    def ability(self, game_state):
        cards = game_state.jostling_cards
        before_panda = True
        cards_before_panda = 0
        cards_after_panda = 0
        for i, card in enumerate(cards):
            if card.id == self.id:
                before_panda = False
            else:
                if before_panda:
                    cards_before_panda += 1
                else:
                    cards_after_panda += 1

        cards_to_kick = cards_before_panda-cards_after_panda
        actions = []
        if cards_to_kick > 0:
            for i in range(cards_to_kick):
                actions.append([Board.kick_by_id, cards[i].id])
        elif cards_to_kick < 0:
            for i in range(cards_to_kick*-1):
                actions.append([Board.kick_by_id, cards[game_state.cards_in_line-i-1].id])
        return actions


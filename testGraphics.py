from enum import Enum
import random

from colorama import init, Fore, Back, Style
init(autoreset=True)


class Colors(Enum):
    Blue = Back.BLUE
    Red = Back.RED
    Green = Back.GREEN
    Yellow = Back.YELLOW
    Grey = Back.WHITE
    Black = Back.BLACK
    Cyan = Back.CYAN
    Magenta = Back.MAGENTA
    LightBlue = Back.LIGHTBLUE_EX
    LightRed = Back.LIGHTRED_EX
    LightGreen = Back.LIGHTGREEN_EX
    LightCyan = Back.LIGHTCYAN_EX
    LightMagenta = Back.LIGHTMAGENTA_EX
    LightYellow = Back.LIGHTYELLOW_EX
    White = Back.LIGHTWHITE_EX


class TestGraphics:

    def __init__(self):
        pass

    @staticmethod
    def generate_general_card(text):
        return text

    @staticmethod
    def generate_card(card):
        return f"{card.full_name} {card.strength}"

    @staticmethod
    def generate_empty_card():
        return 'Empty'

    @staticmethod
    def generate_shadowed_card(card):
        return f"({card.full_name} {card.strength})"

    @staticmethod
    def generate_empty_shadowed_card():
        return '(Empty)'

    @staticmethod
    def concat_cards(text_cards):
        return text_cards

    def display_board(self, game_state):
        if not game_state.card_in_sky:
            print(self.concat_cards([self.generate_general_card('Sky')]))
        else:
            print(self.concat_cards([self.generate_card(game_state.card_in_sky)]))
        jostling_cards = game_state.jostling_area
        board_cards = [self.generate_general_card('The Bar!!')]
        for card in jostling_cards:
            if card:
                board_cards.append(self.generate_card(card))
            else:
                board_cards.append(self.generate_empty_card())

        board_cards.append(self.generate_general_card('The Trash'))
        if not game_state.card_in_back_ally:
            board_cards.append(self.generate_general_card('Back Ally'))
        else:
            board_cards.append(self.generate_card(game_state.card_in_back_ally))

        board = self.concat_cards(board_cards)
        print(board)

        shadow_cards = [self.generate_empty_shadowed_card()]
        for card in game_state.jostling_area:
            if card:
                if card.shadowed_card:
                    shadow_cards.append(self.generate_shadowed_card(card.shadowed_card))
                else:
                    shadow_cards.append(self.generate_empty_shadowed_card())
            else:
                shadow_cards.append(self.generate_empty_shadowed_card())
        print(self.concat_cards(shadow_cards))

    def display_hand(self, hand, amount_in_deck, color):
        text_cards = []
        for card in hand:
            if card:
                text_cards.append(self.generate_card(card))
            else:
                text_cards.append(self.generate_empty_card())
        text_cards.append(self.generate_general_card(f" Deck ({str(amount_in_deck).zfill(2)})"))

        concat_cards = self.concat_cards(text_cards)
        print(concat_cards)

    @staticmethod
    def display_stats(game_state):
        print('')
        cards_in_trash = {}

        for card in game_state.trash:
            try:
                cards_in_trash[card.color.name] += 1
            except KeyError:
                cards_in_trash[card.color.name] = 1

        print(game_state.trash)
        string = "   | Trash (amount of cards)\n"
        for key in cards_in_trash.keys():
            string += f"{str(cards_in_trash[key]).zfill(2)} |{Colors[key].value}{' '*cards_in_trash[key]}{Back.RESET}\n"

        print(string)

        cards_in_bar = {}

        for card in game_state.bar:
            try:
                cards_in_bar[card.color.name] += card.vp
            except KeyError:
                cards_in_bar[card.color.name] = card.vp

        print(game_state.bar)
        string = "   | Bar (amount of VP)\n"
        for key in cards_in_bar.keys():
            string += f"{str(cards_in_bar[key]).zfill(2)} |{Colors[key].value}{' ' * cards_in_bar[key]}{Back.RESET}\n"

        print(string)

    @staticmethod
    def get_card(game_state):
        index = random.randrange(0, game_state.cards_in_line)
        return game_state.jostling_area[index]

    @staticmethod
    def get_card_from_hand(hand):
        hand_len = len(hand)
        if hand_len == 0:
            return None

        else:
            index = random.randrange(0, hand_len)
            return index

    @staticmethod
    def get_bat_input(game_state):
        while True:
            index = random.randrange(0, game_state.cards_in_line)
            if game_state.jostling_area[index].name != 'Bat':
                return game_state.jostling_area[index].id

    @staticmethod
    def get_sloth_input(game_state):
        indexes = []
        for i, card in enumerate(game_state.jostling_cards):
            if card.recurring_action or card.permanent_action:
                indexes.append(i)
        if len(indexes) == 0:
            return -1
        index = random.choice(indexes)
        return index

    @staticmethod
    def get_chameleon_input(game_state):
        while True:
            index = random.randrange(0, game_state.cards_in_line)
            if game_state.jostling_area[index].name != 'Chameleon' and game_state.jostling_area[index].name != 'Eagle' and game_state.jostling_area[index].name != 'Camel':
                print(f"c index {index}")
                return index

    @staticmethod
    def get_panda_input(game_state):
        index = random.randrange(0, game_state.cards_in_line)
        return index

    @staticmethod
    def get_strength(game_state):
        while True:
            strength = random.randint(0, 12)
            for card in game_state.jostling_cards:
                if card.strength == strength:
                    return strength

    @staticmethod
    def get_kangaroo_input():
        spaces = random.randint(1, 2)
        return spaces

    @staticmethod
    def get_ostrich_input():
        even = random.randint(0, 1)
        return even == 0

    @staticmethod
    def get_all_cards_of_strength_input(game_state, strength):
        ids = []
        for card in game_state.jostling_cards:
            if card.strength == strength:
                ids.append(card.id)

        random_id = random.choice(ids)
        return random_id


if __name__ == "__main__":
    pass

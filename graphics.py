from enum import Enum

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


class CMDGraphics:

    def __init__(self):
        pass

    @staticmethod
    def generate_general_card(color=Colors.Grey, text_color=Fore.BLACK, first_line="", second_line="", third_line="", forth_line="", fifth_line="", sixth_line=""):
        width = 11
        card = [
            f"{text_color}{color.value}┌{'-' * width}┐{Back.RESET}{Fore.RESET}",
            f"{text_color}{color.value}|{first_line.ljust(width)}|{Back.RESET}{Fore.RESET}",
            f"{text_color}{color.value}|{second_line.ljust(width)}|{Back.RESET}{Fore.RESET}",
            f"{text_color}{color.value}|{third_line.ljust(width)}|{Back.RESET}{Fore.RESET}",
            f"{text_color}{color.value}|{forth_line.ljust(width)}|{Back.RESET}{Fore.RESET}",
            f"{text_color}{color.value}|{fifth_line.ljust(width)}|{Back.RESET}{Fore.RESET}",
            f"{text_color}{color.value}|{' ' * width}|{Back.RESET}{Fore.RESET}",
            f"{text_color}{color.value}└{'-' * width}┘{Back.RESET}{Fore.RESET}"
        ]
        return card

    @staticmethod
    def generate_card(card):
        width = 11
        recurring = '@' if card.recurring_action else ' '
        permanent = '#' if card.permanent_action else ' '
        card = [
            f"{Fore.BLACK}{card.color.value}┌{'-'*width}┐{Back.RESET}{Fore.RESET}",
            f"{Fore.BLACK}{card.color.value}| {str(card.strength).zfill(2)} {recurring} {permanent}  {card.vp} |{Back.RESET}{Fore.RESET}",
            f"{Fore.BLACK}{card.color.value}| {''.ljust(width - 1)}|{Back.RESET}{Fore.RESET}",
            f"{Fore.BLACK}{card.color.value}| {card.name[:9].ljust(width-1)}|{Back.RESET}{Fore.RESET}",
            f"{Fore.BLACK}{card.color.value}| {card.color.name[:9].ljust(width-1)}|{Back.RESET}{Fore.RESET}",
            f"{Fore.BLACK}{card.color.value}| {str(card.card_type.name)[:9].ljust(width-1)}|{Back.RESET}{Fore.RESET}",
            f"{Fore.BLACK}{card.color.value}|{' ' * width}|{Back.RESET}{Fore.RESET}",
            f"{Fore.BLACK}{card.color.value}└----{f'({card.index+1})' if card.index is not None else '---'}----┘{Back.RESET}{Fore.RESET}"
        ]
        return card

    def generate_empty_card(self, color=Colors.Grey):
        return self.generate_general_card(color, third_line='   Empty')

    @staticmethod
    def generate_shadowed_card(card):
        width = 11
        recurring = '@' if card.recurring_action else ' '
        permanent = '#' if card.permanent_action else ' '
        card = [
            f"{Fore.BLACK}{card.color.value}┌ {str(card.strength).zfill(2)} {recurring} {permanent}  {card.vp} ┐{Back.RESET}{Fore.RESET}",
            f"{Fore.BLACK}{card.color.value}| {card.name[:9].ljust(width - 1)}|{Back.RESET}{Fore.RESET}",
            f"{Fore.BLACK}{card.color.value}└ {card.color.name[:9].ljust(width - 1)}┘{Back.RESET}{Fore.RESET}",
        ]
        return card

    @staticmethod
    def generate_empty_shadowed_card():
        width = 11
        card = [f"{' '*(width+2)}"]*3
        return card

    @staticmethod
    def concat_cards(text_cards):
        spaces = 1
        string = ""
        for line in range(len(text_cards[0])):
            for card in text_cards:
                string += card[line]
                string += " "*spaces
            string += '\n'

        return string

    def display_board(self, game_state):
        if not game_state.card_in_sky:
            print(self.concat_cards([self.generate_general_card(text_color=Fore.GREEN, third_line='    Sky')]))
        else:
            print(self.concat_cards([self.generate_card(game_state.card_in_sky)]))
        jostling_cards = game_state.jostling_area
        board_cards = [self.generate_general_card(text_color=Fore.RED, third_line=' The Bar!!', forth_line=f'   ({str(len(game_state.bar)).zfill(2)})')]
        for card in jostling_cards:
            if card:
                board_cards.append(self.generate_card(card))
            else:
                board_cards.append(self.generate_empty_card())

        board_cards.append(self.generate_general_card(text_color=Fore.BLUE, third_line=' The Trash', forth_line=f'   ({str(len(game_state.trash)).zfill(2)})'))
        if not game_state.card_in_back_ally:
            board_cards.append(self.generate_general_card(text_color=Fore.YELLOW, third_line=' Back Ally'))
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
        text_cards.append(self.generate_general_card(color, third_line=f" Deck ({str(amount_in_deck).zfill(2)})"))

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
        while True:
            try:
                index = int(input(f"Choose an index (1-{game_state.cards_in_line-1}): "))
                if 1 <= index <= game_state.cards_in_line:
                    return game_state.jostling_area[index-1]
                else:
                    print(f"{index} - is not between 1-{game_state.cards_in_line-1}, please choose again.")

            except ValueError:
                print("Your input is not a valid integer, please enter a valid input")

    @staticmethod
    def get_card_from_hand(hand):
        hand_len = len(hand)
        if hand_len == 0:
            return None

        else:
            while True:
                try:
                    index = int(input(f"Choose an index (1-{hand_len}): "))
                    if 1 <= index <= hand_len:
                        return index - 1
                    else:
                        print(f"{index} - is not between 1-{hand_len}, please choose again.")

                except ValueError:
                    print("Your input is not a valid integer, please enter a valid input")

    @staticmethod
    def get_bat_input(game_state):
        while True:
            try:
                index = int(input(f"Choose an index (1-{game_state.cards_in_line}): "))
                if 1 <= index <= game_state.cards_in_line and game_state.jostling_area[index - 1].name != 'Bat':
                    return game_state.jostling_area[index - 1].id
                else:
                    print(f"{index} - is not between 1-{game_state.cards_in_line}, please choose again.")

            except ValueError:
                print("Your input is not a valid integer, please enter a valid input")

    @staticmethod
    def get_sloth_input(game_state):
        indexes = []
        for i, card in enumerate(game_state.jostling_cards):
            if card.recurring_action or card.permanent_action:
                indexes.append(i)
        if len(indexes) == 0:
            return -1
        elif len(indexes) == 1:
            return indexes[0]
        while True:
            try:
                index = int(input(f"Choose an index (0-{game_state.cards_in_line - 1}): "))
                if index in indexes:
                    return index
                else:
                    print(f"{index} - is not between 0-{game_state.cards_in_line - 1}, please choose again.")

            except ValueError:
                print("Your input is not a valid integer, please enter a valid input")

    @staticmethod
    def get_chameleon_input(game_state):
        while True:
            try:
                index = int(input(f"Choose an index (1-{game_state.cards_in_line}): "))
                if 1 <= index <= game_state.cards_in_line and game_state.jostling_area[index-1].name != 'Chameleon' and game_state.jostling_area[index].name != 'Eagle' and game_state.jostling_area[index].name != 'Camel':
                    return index-1
                else:
                    print(f"{index} - is not between 1-{game_state.cards_in_line}, please choose again.")

            except ValueError:
                print("Your input is not a valid integer, please enter a valid input")

    @staticmethod
    def get_panda_input(game_state):
        while True:
            try:
                index = int(input(f"Choose an index (1-{game_state.cards_in_line - 1}): "))
                if 0 < index < game_state.cards_in_line:
                    return index
                else:
                    print(f"{index} - is not between 1-{game_state.cards_in_line - 1}, please choose again.")

            except ValueError:
                print("Your input is not a valid integer, please enter a valid input")

    @staticmethod
    def get_strength(game_state):
        while True:
            try:
                strength = int(input("Choose strength: "))
                for card in game_state.jostling_cards:
                    if card.strength == strength:
                        return strength
                else:
                    if game_state.card_in_sky:
                        if game_state.card_in_sky.strength == strength:
                            return strength

                print("There are no cards with that strength in the board")

            except ValueError:
                print("Your input is not a valid integer, please enter a valid input")

    @staticmethod
    def get_kangaroo_input():
        while True:
            try:
                spaces = int(input("Do you want to jump 1 or 2 spaces? "))
                if 1 <= spaces <= 2:
                    return spaces

                print("Too many spaces!")

            except ValueError:
                print("Your input is not a valid integer, please enter a valid input")

    @staticmethod
    def get_ostrich_input():
        while True:
            even = input("Do you want to skip the ODD cards (O) or EVEN (E)? ").upper()
            if even == 'E' or even == 'O':
                return even == 'E'
            else:
                print(f'{even} is not one of the options (E - evens, O - Odds)')

    @staticmethod
    def get_all_cards_of_strength_input(game_state, strength):
        ids = []
        for card in game_state.jostling_cards:
            if card.strength == strength:
                ids.append(card.id)

        while True:
            try:
                index = int(input(f"Choose a card from the list {ids}"))
                if 1 <= index <= len(ids):
                    return ids[index - 1]
                else:
                    print(f'{index} is not one of the options (1 - {len(ids)})')

            except ValueError:
                print("Your input is not a valid integer, please enter a valid input")


if __name__ == "__main__":
    pass

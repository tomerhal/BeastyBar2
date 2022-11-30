from enum import Enum
from colorama import init, Fore, Back, Style
init(autoreset=True)


class CardTypes(Enum):
    Undefined = 0
    Big_Bruiser = 1
    Little_Bully = 2
    Doppelganger = 3
    Trampler = 4
    Shield = 5


class Card:

    def __init__(self, strength, name, vp=2, recurring_action=False, permanent_action=False, card_type=CardTypes.Undefined, game_edition=0):
        """
        A base class for all cards.
        :param strength: A value of the card that is unique to each card in a deck.
        :param name: The name of the card.
        :param vp: The amount of victory point the card will grant the player when it gets into the bar.
        :param recurring_action: Does this card have a recurring ability?
        :param permanent_action: Does this card have a permanent ability?
        :param card_type: The type of the card (from cardTypes enum), relevant for some abilities in the game.
        :param game_edition:  The game edition of the card has no practical relevance, but it's good to know.
        """
        self._strength = strength
        self._name = name
        self._vp = vp
        self._recurring_action = recurring_action
        self._permanent_action = permanent_action
        self._card_type = card_type
        self._game_edition = game_edition
        self._player = None  # The player that that card belongs to.
        self._index = None  # The index of the card is where it's located within the jostling area (when it is).
        self._color = None
        self._id = None  # The id of the card (it's color + name) is a unique value for each card in the game.
        self._full_name = None
        self.shadowed_card = None
        self.imitating = False
        self.imitated_card = None

    @property
    def strength(self):
        return self.imitated_card.strength if self.imitating else self._strength

    @property
    def name(self):
        return self.imitated_card.name if self.imitating else self._name

    @property
    def vp(self):
        return self.imitated_card.vp if self.imitating else self._vp

    @property
    def recurring_action(self):
        return self.imitated_card.recurring_action if self.imitating else self._recurring_action

    @property
    def permanent_action(self):
        return self.imitated_card.permanent_action if self.imitating else self._permanent_action

    @property
    def card_type(self):
        return self.imitated_card.card_type if self.imitating else self._card_type

    @property
    def game_edition(self):
        return self.imitated_card.game_edition if self.imitating else self._game_edition

    @property
    def color(self):
        return self.imitated_card.color if self.imitating else self._color

    @color.setter
    def color(self, color):
        self._color = color

    @property
    def full_name(self):
        self._full_name = self.color.name + " " + self.name
        return self._full_name

    @property
    def id(self):
        self._id = self.color.name + self.name
        return self._id

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        self._player = player
        self.color = self._player.color

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index
        if self.shadowed_card:
            self.shadowed_card.index = index

    def imitate(self, card):
        self.imitating = True
        self.imitated_card = card

    def reveal(self):
        self.imitating = False

    def place(self, game_state):
        return []

    def ability(self, game_state):
        return self.imitated_card.ability(game_state) if self.imitating else []

    def recurring_ability(self, game_state):
        return self.ability(game_state)

    def stopping_condition(self, card):
        pass

    def permanent_ability(self, card):
        return []

    def permanent_ability_interactional_trigger(self, card):
        return False

    def permanent_ability_positional_trigger(self):
        return False

    def full_jostling_area_ability(self, game_state):
        pass

    def __str__(self):
        recurring = '@' if self.recurring_action else ' '
        permanent = '#' if self.permanent_action else ' '
        try:
            color = self.color.value
            color_name = self.color.name
        except AttributeError:
            color = Back.WHITE
            color_name = 'unassigned'
        string = Fore.BLACK + f"""\n{color}┌{"-"*12}┐{Back.RESET}
{color}| {str(self.strength).zfill(2)} {recurring} {permanent}   {self.vp} |{Back.RESET}
{color}|{" "*12}|{Back.RESET}
{color}| {self.name[:10].ljust(10)} |{Back.RESET}
{color}| {color_name[:10].ljust(10)} |{Back.RESET}
{color}| {str(self.card_type.name)[:10].ljust(10)} |{Back.RESET}
{color}|{" "*12}|{Back.RESET}
{color}└{"-"*12}┘{Back.RESET}\n""" + Fore.RESET
        return string

    def __repr__(self):
        return self.id

    @staticmethod
    def compare(card):
        if card:
            return card.strength
        else:
            return -1

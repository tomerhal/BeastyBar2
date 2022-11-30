import copy
import random

"""
The board layout:

|           |                               
|           |                               
|  The Sky  |                               
|           |                               
|           |                               

|           |   | --------------------- Jostling Area --------------------- |   |           | |           |
|           |   |          ||           ||          ||          ||          |   |           | |           |
| The Bar!! |<==| 1st Spot ||  2nd Spot || 3rd Spot || 4th Spot || 5th Spot |==>| Trash :-( | | Back Ally |
|           |   |          ||           ||          ||          ||          |   |           | |           |
|           |   |          ||           ||          ||          ||          |   |           | |           |
                -------------------------------------------------------------
                |          ||           ||          ||          ||          |
                |          ||           ||          ||          ||          |
                | ----------------------- Shadows ------------------------- |

"""


class Player:

    def __init__(self, name, color, deck, graphics_engine, seed=5):
        """
        Player is a class handling user cards.
        :param name: The name of the player.
        :param color: The color of the player cards.
        :param deck: The cards the player has chose as his deck.
        :param graphics_engine: The type of user interface to display the game in.
        """
        self.name = name
        self.color = color
        self.deck = deck
        self.deck_len = len(self.deck)
        self.graphics_engine = graphics_engine()
        for card in deck:
            card.player = self
        print(f"{name}'s seed is: {seed}")
        random.seed(seed)
        random.shuffle(deck)
        self.hand = []
        for i in range(4):
            self.draw()

    def draw(self):
        """
        Taking a card from the deck and moving it to the hand.
        """
        if len(self.deck) > 0:
            card = self.deck.pop()
            card.index = len(self.hand)
            self.hand.append(card)

    def play_card(self):
        """
        Getting an index from the user of what card to play from hand.
        :return: The selected card.
        """
        index = self.graphics_engine.get_card_from_hand(self.hand)
        played_card = self.hand.pop(index)
        for i in range(played_card.index, len(self.hand)):
            self.hand[i].index -= 1
        return played_card


class Board:
    def __init__(self):
        self.jostling_area_len = 5
        self.jostling_area = [None]*self.jostling_area_len
        self.bar = []
        self.trash = []
        self.card_in_back_ally = None
        self.back_ally_index = 6
        self.card_in_sky = None
        self.sky_index = 7
        self.shadows = [None] * 5

    @property
    def full(self):  # Does the jostling area have 5 cards in it.
        self.regroup_cards()
        return self.cards_in_line == self.jostling_area_len

    @property  # A list of the cards in the jostling area
    def jostling_cards(self):
        return self.jostling_area[:self.cards_in_line]

    @property
    def cards_in_line(self):  # The number of cards in jostling area
        cards = 0
        for card in self.jostling_area:
            if card:
                cards += 1
        return cards

    def reassign_indexes(self):
        """
        reassigning indexes to the cards in the jostling area.
        """
        # print(f"reassign indexes: {self.jostling_area}")
        for i in range(self.cards_in_line):
            self.jostling_area[i].index = i
            if self.shadows[i]:
                self.shadows[i].index = i

    def regroup_cards(self):
        """
        pushing forward all the cards, to make sure there are no spaces between cards, then reassigning indexes.
        """
        # print(f"regrouping: {self.jostling_area}")
        index_offset = 0
        for i in range(self.jostling_area_len):
            if not self.jostling_area[i - index_offset]:
                self.jostling_area.pop(i - index_offset)
                self.jostling_area.append(None)
                self.shadows.pop(i - index_offset)
                self.shadows.append(None)
                index_offset += 1

        self.reassign_indexes()

    def id_to_index(self, card_id):
        """
        Converts a card id, and return it's index in the jostling area
        :param card_id: The id of the card.
        :return: index (int)
        """
        # print(self.jostling_cards)
        for i, card in enumerate(self.jostling_cards):
            if card.id == card_id:
                return i
        else:
            if self.card_in_sky:
                if self.card_in_sky.id == card_id:
                    return 6
            return None

    def get_player_input(self, input_type, player):
        """
        Will be relevant in future releases.
        :param input_type: The type of input the card expects to get from the player.
        :param player: The player who's now playing.
        :return: The input from the player.
        """
        player_input = None
        return player_input

    def switch_2_cards(self, index1, index2=None):  # maybe replaced by 'jump'
        """
        switching position of two cards, mainly used while advancing.
        :param index1: the index of one of the cards
        :param index2: the index of the second card, if not assigned, it will be the next card after 'index 1'
        """
        if not index2:
            index2 = index1-1
        temp = self.jostling_area[index1]
        self.jostling_area[index1] = self.jostling_area[index2]
        self.jostling_area[index2] = temp

    def activate_ability(self, actions):
        """
        Gets a list of actions, and executing them.
        :param actions: A list of actions to execute.
        """
        for action in actions:
            action, *params = action
            action(self, *params)
            self.regroup_cards()

    def place_card(self, card):
        """
        Places a card in the game, activating it's 'join' action, and then activating it's abilities.
        :param card:
        """
        join_action, *params = card.place(game_state=self)
        join_action(self, card, *params)

    def join(self, card, index=-1, activate_ability=True):
        """
        join: places a given card in the jostling area, then activates it's ability.
        :param card: The card to place in the jostling area.
        :param index: Where in the jostling area to put this card, default (-1) is in the first available space.
        :param activate_ability: Should the newly joined card activate his power.
        (0 = closest to the bar, 4 = farthest away from the bar)
        """
        print(f"\n{card.id} has joined the jostling area!\n")
        card.index = self.cards_in_line
        print(card.index, self.jostling_area)
        self.jostling_area[card.index] = card
        if index >= 0:
            self.jump_by_index(card.index, index)
        if activate_ability:
            actions = card.ability(game_state=self)
            self.activate_ability(actions)
        card.reveal()

    def join_back_ally(self, card):
        """
        Placing a card into the back ally.
        :param card: The card to place in the back ally.
        """
        self.card_in_back_ally = card
        actions = card.ability(game_state=self)
        self.activate_ability(actions)

    def fly(self, card_id):
        """
        Moves a card for the jostling area to the sky.
        :param card_id: The id of the card to move.
        """
        card_index = self.id_to_index(card_id)
        card = self.jostling_area.pop(card_index)
        self.jostling_area.append(None)
        self.card_in_sky = card
        self.card_in_sky.index = 6

    def sweep_down(self, dive_index):
        """
        Places the card from the sky in the jostling area, kicking the card in that index (if it does not resist)
        :param dive_index: The index in the jostling area to be placed in.
        """
        other_card = self.jostling_area[dive_index]
        if other_card.permanent_action:
            if other_card.permanent_ability_interactional_trigger(self.card_in_sky):
                # print(f"activating {other_card.id}'s perm ability")
                self.activate_ability(self.jostling_area[dive_index].permanent_ability(self.card_in_sky))
        else:
            self.kick_by_index(dive_index)
            self.join(self.card_in_sky, dive_index, False)
            self.card_in_sky = None

    def jump_by_index(self, card_index, new_index):
        """
        Move a card in a given index to another index in the jostling area.
        :param card_index: The original index of the card to move.
        :param new_index: The new index to move the card to.
        (0 = closest to the bar, 4 = farthest away from the bar)
        """
        # print("jumping", self.jostling_area[card_index].id, new_index)
        card = self.jostling_area.pop(card_index)
        self.jostling_area.insert(new_index, card)

    def jump_by_id(self, card_id, new_index):
        """
        Move a card with a given id to another index in the jostling area.
        :param card_id: The id of the card to move.
        :param new_index: The new index to move the card to.
        (0 = closest to the bar, 4 = farthest away from the bar)
        """
        self.jump_by_index(self.id_to_index(card_id), new_index)

    def jump_to_front(self, card_id):
        """
        Moving a card to the front of the jostling area.
        :param card_id: The id of the card to move.
        """
        self.jump_by_id(card_id, 0)

    def jump_to_back(self, card_id):
        """
        Moving a card to the front of the jostling area.
        :param card_id: The id of the card to move.
        """
        self.jump_by_id(card_id, self.cards_in_line)

    def jump_in_front_of(self, card_to_overtake, card_to_move):
        """
        Moves a card in front of a specific card in the jostling area.
        :param card_to_overtake: The card to move in front of.
        :param card_to_move: The card to move.
        """
        self.jump_by_id(card_to_move, self.id_to_index(card_to_overtake))

    def overtake(self, card_id, cards_to_overtake=1):
        """
        Jumps one space ahead (in contrast to 'advance', overtake don't have stopping conditions).
        :param cards_to_overtake: Number of cards to overtake.
        :param card_id: The id of the card to move.
        """
        card_index = self.id_to_index(card_id)
        self.jump_by_index(card_index, card_index - cards_to_overtake)

    def advance_by_index(self, card_index, kick_overtaken_card=False):
        """
        Moving a card one space at a time, checking every step if that's card stopping condition has been met or
        if the next card has a permanent ability that effects this card movement, then activating that ability.
        :param card_index: The original index of the card to move.
        :param kick_overtaken_card:  should it 'kick' overtaken cards to the 'trash'.
        :return True if the advancement was successful else False
        """
        should_advance = True
        if card_index == 0:
            should_advance = False
        else:
            card_after_next = self.jostling_area[card_index - 2] if card_index > 1 else None
            next_card = self.jostling_area[card_index-1]
            this_card = self.jostling_area[card_index]
            if next_card.permanent_action:
                disabled = False
                if card_after_next:
                    if card_after_next.name == 'Sloth':
                        disabled = card_after_next.permanent_ability_interactional_trigger(next_card)
                        # print(next_card.id, "was disabled", disabled)

                if next_card.permanent_ability_interactional_trigger(this_card) and not disabled:
                    should_advance = False
                    # print(f"activating {next_card.id}'s perm ability")
                    self.activate_ability(self.jostling_area[card_index-1].permanent_ability(this_card))
            if this_card.stopping_condition(next_card):
                should_advance = False

            if should_advance:
                if kick_overtaken_card:
                    self.kick_by_index(card_index - 1)
                else:
                    self.switch_2_cards(card_index)

        return should_advance

    def advance_by_id(self, card_id, kick_overtaken_card=False):
        """
        Advances a card by it's id
        :param card_id: the id of the card to move.
        :param kick_overtaken_card: should the overtaken card be kicked.
        :return: if the advancement was successful
        """
        return self.advance_by_index(self.id_to_index(card_id), kick_overtaken_card)

    def shadow_advance(self, card_id):
        """
        Advances a card, placing the overtaken card in it's shadow.
        :param card_id: the id of the card to move.
        :return: if the advancement was successful.
        """
        should_advance = self.advance_by_id(card_id)
        if should_advance:
            shadow_caster_index = self.id_to_index(card_id)
            prev_caster_index = shadow_caster_index+1
            shadow_caster = self.jostling_area[shadow_caster_index]
            temp = copy.deepcopy(shadow_caster.shadowed_card)
            shadow_caster.shadowed_card = copy.deepcopy(self.jostling_area[prev_caster_index])
            self.jostling_area[prev_caster_index] = temp

        return should_advance

    def advance_to_front(self, card_id, kick_overtaken_card=False):
        """
        Moving a card one space forward at a time, until the end of the jostling area, unless that card stopping
        condition has been met before / a card with relevant permanent ability has been overtaken.
        :param card_id: The id of the card to move.
        :param kick_overtaken_card:  should it 'kick' overtaken cards to the 'trash'.
        """
        card_index = self.id_to_index(card_id)
        # print("advancing", card_index)
        for i in range(card_index):
            if not self.advance_by_id(card_id, kick_overtaken_card):
                # print('advancing has stopped')
                break

    def kick_by_index(self, card_index):
        """
        Sends a card to the trash
        :param card_index: The index of the card to kick
        (0 = closest to the bar, 4 = farthest away from the bar)
        """
        if card_index == 6:
            self.kick_from_sky()
        else:
            print(card_index)
            shadowed_card = self.jostling_area[card_index].shadowed_card
            if shadowed_card:
                shadowed_card.reveal()
                self.trash.append(shadowed_card)

            self.jostling_area[card_index].reveal()
            print("kicking", card_index, self.jostling_area[card_index].id)
            kicked_card = self.jostling_area.pop(card_index)
            self.jostling_area.append(None)
            self.trash.append(kicked_card)

    def kick_by_id(self, card_id):
        """
        kicks a card by it's id
        :param card_id: The id of the card to kick
        """
        # print(card_id)
        self.kick_by_index(self.id_to_index(card_id))

    def kick_last(self):
        """
        Kicks the last card from the jostling area.
        """
        self.kick_by_index(self.cards_in_line - 1)

    def kick_cards(self, indexes):
        """
        Kicks multiple cards.
        :param indexes: the indexes of cards to kick.
        """
        indexes.reverse()
        for index in indexes:
            self.kick_by_index(index)

    def kick_all_by_name(self, card_name, ids_to_skip=[]):
        """
        Kicks all cards of a specific name to the trash.
        :param card_name: The name of cards to kick.
        :param ids_to_skip: id's to spear.
        """
        kicked_cards_indexes = []
        for i, card in enumerate(self.jostling_cards):
            if card.name == card_name and card.id not in ids_to_skip:
                kicked_cards_indexes.append(i)

        self.kick_cards(kicked_cards_indexes)

    def kick_all_by_strength(self, card_strength, ids_to_skip=[]):
        """
        Kicks all cards of a specific strength to the trash.
        :param card_strength: The strength of cards to kick.
        :param ids_to_skip: id's to spear.
        """
        kicked_cards_indexes = []
        for i, card in enumerate(self.jostling_cards):
            if card.strength == card_strength and card.id not in ids_to_skip:
                kicked_cards_indexes.append(i)

        self.kick_cards(kicked_cards_indexes)

    def kick_all_by_type(self, card_type, ids_to_skip=[]):
        """
        Kicks all cards of a specific card type to the trash.
        :param card_type: The type of cards to kick.
        :param ids_to_skip: id's to spear.
        """
        kicked_cards_indexes = []
        for i, card in enumerate(self.jostling_cards):
            if card.card_type == card_type and card.id not in ids_to_skip:
                kicked_cards_indexes.append(i)

        self.kick_cards(kicked_cards_indexes)

    def kick_from_back_ally(self):
        """
        Kicks the card from the  back ally to the trash
        """
        self.card_in_back_ally.reveal()
        self.trash.append(copy.deepcopy(self.card_in_back_ally))
        self.card_in_back_ally = None

    def replace(self, card_to_kick, card_to_replace_with):
        """
        Replaces a card in the jostling area with another card
        :param card_to_kick: The card id of the card to replace.
        :param card_to_replace_with: The card id of the card to place instead.
        """

        self.jump_by_id(card_to_replace_with, self.id_to_index(card_to_kick)+1)
        self.kick_by_id(card_to_kick)

    def kick_from_sky(self):
        """
        Kicks the card in the sky to the trash
        """
        self.card_in_sky.reveal()
        self.trash.append(copy.deepcopy(self.card_in_sky))
        self.card_in_sky = None

    def revive(self):
        """
        Placing the last kicked card to the jostling area and activating it's ability.
        """
        rev_card = self.trash.pop(-1)
        print(f"reviving: {rev_card.full_name}")
        self.place_card(rev_card)

    def revive_enter(self):
        rev_card = self.trash.pop(-1)
        self.jostling_area.append(None)
        self.bar.append(rev_card)
        self.regroup_cards()
        return rev_card

    def enter_by_index(self, card_index):
        """
        Moving a card in jostling area inside the 'Bar' and adding it's VP to the relevant player score
        :param card_index: The index of card to enter.
        :return The card that entered the bar
        """
        shadowed_card = self.jostling_area[card_index].shadowed_card
        if shadowed_card:
            shadowed_card.reveal()
            self.bar.append(shadowed_card)

        self.jostling_area[card_index].reveal()
        print("entering", card_index, self.jostling_area[card_index].id)
        entering_card = self.jostling_area.pop(card_index)
        self.jostling_area.append(None)
        self.bar.append(entering_card)
        self.regroup_cards()
        return entering_card

    def enter_by_id(self, card_id):
        """
        Letting the card with that id into the bar.
        :param card_id: The card to enter into the bar.
        :return The card that entered the bar
        """
        return self.enter_by_index(self.id_to_index(card_id))

    def enter_first(self):
        """
        Moving the first card in jostling area to the 'Bar'.
        :return The card that entered the bar (should be the first card in the jostling area).
        """
        return self.enter_by_index(0)

    def enter_from_back_ally(self):
        """
        Letting the card from the back ally into the bar.
        :return: The card from the back ally
        """
        entering_card = copy.deepcopy(self.card_in_back_ally)
        self.bar.append(entering_card)
        self.card_in_back_ally = None
        return entering_card

    def reorder(self, new_indexes):
        """
        Reordering the cards in the jostling area according to the new indexes.
        :param new_indexes: The new indexes of the cards in jostling area.
        """
        # print("reordering", new_indexes)
        temp = copy.deepcopy(self.jostling_area)
        for i, new_index in enumerate(new_indexes):
            # print(self.cards[i].name, " <- ", temp[new_index].name)
            self.jostling_area[i] = temp[new_index]

    def activate_recurring(self, card):
        """
        Activating all recurring abilities in the jostling area by order (closets to 'bar' first).
        :param card: The last played card, in case that card is have a recurring ability (so it wont be activated twice).
        """
        print("------- ACTIVATING RECURRING ABILITIES ---------\n")
        # for i in range(self.cards_in_line):
        #     if i > self.cards_in_line - 1:
        #         # print('breaking of recurring activation')
        #         break
        #     if self.jostling_area[i].recurring_action and self.jostling_area[i] != card:
        #         # print(self.jostling_area[i].id)
        #         self.activate_ability(self.jostling_area[i].recurring_ability(self))
        for other_card in self.jostling_cards:
            if other_card.recurring_action and other_card != card:
                # print(self.jostling_area[i].id)
                self.activate_ability(other_card.recurring_ability(self))

    def activate_positional_permanent(self):
        """
        Activating all positional based permanent abilities in the jostling area by order (closets to 'bar' first).
        """
        print("------- ACTIVATING POSITIONAL ABILITIES ---------\n")
        for i in range(self.cards_in_line):
            if i > self.cards_in_line - 1:
                # print('breaking of recurring activation')
                break
            if self.jostling_area[i].permanent_action and self.jostling_area[i].permanent_ability_positional_trigger():
                # print(self.jostling_area[i].id)
                self.activate_ability(self.jostling_area[i].permanent_ability(self))


class Game:

    def __init__(self, players, deck_len):
        self.players = players
        try:
            for player in players:
                if player.deck_len != deck_len:
                    raise Exception("Failed to initialize game because not all players have the same size deck!")

            self.deck_len = deck_len
            self.board = Board()
            self.scores = {}
            for player in players:
                self.scores[player.color.name] = 0

        except Exception as e:
            print(e)

        self.main_loop()

    def turn(self, player):
        player.graphics_engine.display_board(self.board)
        player.graphics_engine.display_hand(player.hand, len(player.deck), player.color)
        # 1. The player places a card from their hand, activating it's ability. (in this stage there can be user input)
        card = player.play_card()
        print(player.name, "has chosen to play", card.full_name)
        self.board.place_card(card)
        player.graphics_engine.display_board(self.board)
        # 2. The player will draw a new card from the deck (if possible).
        player.draw()
        player.graphics_engine.display_hand(player.hand, len(player.deck), player.color)
        # 3. Then, all Recurring abilities will be activated in order, from the front of the line backwards.
        self.board.activate_recurring(card)
        player.graphics_engine.display_board(self.board)
        # 3.5 Check for permanent abilities with positional triggers
        self.board.activate_positional_permanent()
        player.graphics_engine.display_board(self.board)
        # 4. Empty the back ally (if there is a card in it)
        if self.board.card_in_back_ally:
            self.board.kick_from_back_ally()
            player.graphics_engine.display_board(self.board)
        # 5. Then, Check for 5 cards in jostling area. If true, "open heavens gate", else - next turn.
        # print('full?', self.board.full)
        if self.board.full:
            # 6. Opening havens gate:
            #   6.1. check for relevant abilities.
            if self.board.card_in_sky:
                self.board.activate_ability(self.board.card_in_sky.full_jostling_area_ability(self.board))
                player.graphics_engine.display_board(self.board)
            #   6.2. the two most forward cards will enter the bar.
            #   6.3. the last card in the jostling area will be kicked to the trash.
            self.open_heavens_gate()
            player.graphics_engine.display_board(self.board)
        player.graphics_engine.display_stats(self.board)
        # 7. end game conditions: all of the players have played all of their cards.

    def main_loop(self):
        for i in range(self.deck_len):  # should be 12 / 13
            for player in self.players:
                self.turn(player)

        winner = self.winner()
        if len(winner) == 1:
            print(f"The winner is the {winner[0].title()} player!")
        elif len(winner) == 0:
            print("There are no winners this time :(")
        else:
            print(f"The winners are the {[player.title()+'and ' for player in winner]} \b\b\b\bplayers")

    def open_heavens_gate(self):
        print("OPENING HEAVENS GATE!!!")
        self.board.kick_last()
        for i in range(2):
            entering_card = self.board.enter_first()
            self.add_to_score(entering_card)
            self.players[0].graphics_engine.display_board(self.board)

    def add_to_score(self, card):
        """
        Adds the vp of the card that entered the bar to the score of each player
        :param card: The card to that entered the bar.
        """
        self.scores[card.color.name] += card.vp

    def winner(self):
        """
        Checks who won.
        :return: A list of the names of the winners.
        """
        winner = []
        max_score = 1
        for key in self.scores.keys():
            if self.scores[key] > max_score:
                winner = [key]
                max_score = self.scores[key]
            elif self.scores[key] == max_score:
                winner.append(key)

        return winner

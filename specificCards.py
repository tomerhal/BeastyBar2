import random
import copy

from card import *
from board import Board


# ---------------------------------------------- Original (first edition) ----------------------------------------------

class Lion(Card):  # Done

    def __init__(self):
        super().__init__(12, "Lion", 2, False, False, CardTypes.Undefined, 1)

    def ability(self, game_state):
        actions = []
        other_lion = False
        for i, card in enumerate(game_state.jostling_cards):
            if card.name == "Lion" and card.color != self.color:
                actions.append([Board.kick_last])
                other_lion = True
            elif card.name == "Monkey":
                actions.append([Board.kick_by_index, i])
        actions.reverse()
        if not other_lion:
            for action in actions:
                action[1] += 1
            actions.insert(0, [Board.jump_to_front, self.index])
        return actions


class Hippo(Card):  # Done

    def __init__(self):
        super().__init__(11, "Hippo", 2, True, False, CardTypes.Trampler, 1)

    def ability(self, game_state):
        return [[Board.advance_to_front, self.index]]

    def stopping_condition(self, card):
        return card.strength >= self.strength


class Crocodile(Card):  # Done

    def __init__(self):
        super().__init__(10, "Crocodile", 3, True, False, CardTypes.Big_Bruiser, 1)

    def ability(self, game_state):
        return [[Board.advance_to_front, self.index, True]]

    def stopping_condition(self, card):
        return card.strength >= self.strength or card.card_type == CardTypes.Shield


class Snake(Card):  # Done

    def __init__(self):
        super().__init__(9, "Snake", 2, False, False, CardTypes.Undefined, 1)

    def ability(self, game_state):
        jostling_copy = copy.deepcopy(game_state.jostling_cards)
        jostling_copy.sort(key=Card.compare, reverse=True)
        new_indexes = []
        for card in jostling_copy:
            new_indexes.append(card.index)
        # print("new indexes", new_indexes)
        return [[Board.reorder, new_indexes]]


class Giraffe(Card):  # Done

    def __init__(self,):
        super().__init__(8, "Giraffe", 3, True, False, CardTypes.Undefined, 1)

    def ability(self, game_state):
        return [[Board.advance_by_index, self.index]]

    def stopping_condition(self, card):
        return card.strength >= self.strength


class Zebra(Card):  # Done

    def __init__(self):
        super().__init__(7, "Zebra", 4, False, True, CardTypes.Shield, 1)

    def permanent_ability_interactional_trigger(self, card):
        return card.card_type == CardTypes.Big_Bruiser or card.card_type == CardTypes.Trampler


class Seal(Card):  # Done

    def __init__(self):
        super().__init__(6, "Seal", 2, False, False, CardTypes.Undefined, 1)

    def ability(self, game_state):
        new_indexes = []
        for card in game_state.jostling_cards:
            new_indexes.insert(0, card.index)
        return [[Board.reorder, new_indexes]]


class Chameleon(Card):

    def __init__(self):
        super().__init__(5, "Chameleon", 3, False, False, CardTypes.Shield, 1)

    def legal_actions(self,jostling_area,hand):
        actions = []
        for card in jostling_area:
            if card.name != self.name and (self.name + " " + card.name) not in actions:
                actions.append(self.name + " " + card.name)
        if actions is []:
            return [self.name]



class Monkey(Card):  # Done

    def __init__(self):
        super().__init__(4, "Monkey", 3, False, False, CardTypes.Undefined, 1)

    def ability(self, game_state):
        monkey_indexes = []
        kick_indexes = []
        other_monkeys = False
        for i, card in enumerate(game_state.jostling_cards):
            if card.name == self.name and card.color != self.color:
                monkey_indexes.append(i)
                other_monkeys = True
            if card.card_type == CardTypes.Big_Bruiser or card.card_type == CardTypes.Trampler:
                kick_indexes.append(i)
        actions = []
        if other_monkeys:
            for index in kick_indexes:
                actions.append([Board.kick_by_index, index])
            actions.append([Board.jump_by_index, self.index, 0])
            for i, index in enumerate(monkey_indexes):
                actions.append([Board.jump_by_index, index + 1, i + 1])  # index + 1 because the first monkey jumps ahead pushing every one back.
        return actions


class Kangaroo(Card):

    def __init__(self):
        super().__init__(3, "Kangaroo", 4, False, False, CardTypes.Undefined, 1)


class Parrot(Card):

    def __init__(self):
        super().__init__(2, "Parrot", 4, False, False, CardTypes.Little_Bully, 1)


class Skunk(Card):  # Done

    def __init__(self):
        super().__init__(1, "Skunk", 4, False, False, CardTypes.Little_Bully, 1)

    def ability(self, game_state):
        highest_strength = -1
        second_highest_strength = -1
        for card in game_state.jostling_cards:
            strength = card.strength
            if strength > highest_strength and card.name != self.name:
                second_highest_strength = highest_strength
                highest_strength = strength
            elif highest_strength > strength > second_highest_strength and card.name != self.name:
                second_highest_strength = strength

        if second_highest_strength >= 0:
            return [[Board.kick_all_by_strength, highest_strength], [Board.kick_all_by_strength, second_highest_strength]]
        elif highest_strength >= 0:
            return [[Board.kick_all_by_strength, highest_strength]]
        return []


# ----------------------------------------- NEW BEAST IN TOWN (second edition) -----------------------------------------

class Rhino(Card):

    def __init__(self):
        super().__init__(12, "Rhino", 3, False, False, CardTypes.Big_Bruiser, 2)

    def ability(self, game_state):
        pass


class Bear(Card):  # Done

    def __init__(self):
        super().__init__(11, "Bear", 2, False, False, CardTypes.Big_Bruiser, 2)

    def ability(self, game_state):
        lowes_strength = 13
        second_lowes_strength = 13
        for card in game_state.jostling_cards:
            if card.id != self.id:
                strength = card.strength
                if strength < lowes_strength:
                    second_lowes_strength = lowes_strength
                    lowes_strength = strength
                elif lowes_strength < strength < second_lowes_strength:
                    second_lowes_strength = strength

        actions = []
        jump_offset = 0
        for i, card in enumerate(game_state.jostling_cards):
            if card.strength <= second_lowes_strength and card.id != self.id:
                actions.append([Board.jump_to_back, i-jump_offset])
                jump_offset += 1

        # print(actions, f'low = {lowes_strength}, sec low = {second_lowes_strength}')
        return actions


class Tiger(Card):  # Done

    def __init__(self):
        super().__init__(10, "Tiger", 3, True, False, CardTypes.Big_Bruiser, 2)

    def ability(self, game_state):
        actions = []
        if self.index == 1:
            actions = [[Board.jump_by_index, 1, 0]]
        elif self.index > 1 and not self.stopping_condition(game_state.jostling_cards[self.index-1]):
            actions = [[Board.jump_by_index, self.index, self.index - 1], [Board.advance_by_index, self.index - 1, True]]

        return actions

    def recurring_ability(self, game_state):
        return [[Board.advance_by_index, self.index, True]]

    def stopping_condition(self, card):
        return card.strength >= self.strength or card.card_type == CardTypes.Shield


class Cheetah(Card):

    def __init__(self):
        super().__init__(9, "Cheetah", 4, False, False, CardTypes.Big_Bruiser, 2)

    def ability(self, game_state):
        pass


class Llama(Card):  # Done

    def __init__(self):
        super().__init__(8, "Llama", 4, True, False, CardTypes.Undefined, 2)

    def ability(self, game_state):
        actions = []
        if self.index > 0 and not self.stopping_condition(game_state.jostling_cards[self.index-1]):
            actions = [[Board.jump_to_back, self.index-1]]
        return actions

    def stopping_condition(self, card):
        return card.strength >= self.strength


class Porcupine(Card):  # Done

    def __init__(self):
        super().__init__(7, "Porcupine", 4, False, True, CardTypes.Shield, 2)

    def permanent_ability(self, card):
        return [[Board.kick_by_index, card.index]]

    def permanent_ability_interactional_trigger(self, card):
        return card.card_type == CardTypes.Big_Bruiser


class Ostrich(Card):

    def __init__(self):
        super().__init__(6, "Ostrich", 3, False, False, CardTypes.Undefined, 2)

    def ability(self, game_state):
        pass


class Penguin(Card):

    def __init__(self):
        super().__init__(5, "Penguin", 3, False, False, CardTypes.Doppelganger, 2)

    def ability(self, game_state):
        pass


class Dog(Card):  # Done

    def __init__(self):
        super().__init__(4, "Dog", 2, False, False, CardTypes.Undefined, 2)

    def ability(self, game_state):
        jostling_copy = copy.deepcopy(game_state.jostling_cards)
        jostling_copy.sort(key=Card.compare)
        new_indexes = []
        for card in jostling_copy:
            new_indexes.append(card.index)
        return [[Board.reorder, new_indexes]]


class Peacock(Card):

    def __init__(self):
        super().__init__(3, "Peacock", 2, False, False, CardTypes.Undefined, 2)

    def ability(self, game_state):
        pass


class Vulture(Card):  # Done

    def __init__(self):
        super().__init__(2, "Vulture", 2, False, False, CardTypes.Doppelganger, 2)

    def ability(self, game_state):
        if len(game_state.trash) > 0:
            card_to_rev = game_state.trash[-1]
            if card_to_rev.name == self.name:
                return [[Board.go_to_back_ally, self.index], [Board.revive, False], [Board.enter_by_index, game_state.cards_in_line - 1], [Board.enter_from_back_ally]]
            else:
                return [[Board.go_to_back_ally, self.index], [Board.revive]]
        else:
            return [[Board.go_to_back_ally, self.index]]


class Bat(Card):

    def __init__(self):
        super().__init__(1, "Bat", 4, False, True, CardTypes.Little_Bully, 2)

    def ability(self, game_state):
        pass

    def permanent_ability(self, game_state):
        pass

    def permanent_ability_interactional_trigger(self, card):
        pass


# ------------------------------------------ Born to by wild (third edition) ------------------------------------------

class Elephant(Card):  # Done

    def __init__(self):
        super().__init__(12, "Elephant", 3, False, False, CardTypes.Undefined, 3)

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
        return [[Board.jump_by_index, self.index, max(self.index - spaces_to_jump, 0)]]


class Camel(Card):

    def __init__(self):
        super().__init__(11, "Camel", 2, True, False, CardTypes.Trampler, 3)

    def ability(self, game_state):
        pass

    def recurring_ability(self, game_state):
        pass

    def stopping_condition(self, card):
        pass


class Buffalo(Card):  # Done

    def __init__(self):
        super().__init__(10, "Buffalo", 3, True, False, CardTypes.Big_Bruiser, 3)

    def ability(self, game_state):
        return [[Board.advance_by_index, self.index, True]]

    def stopping_condition(self, card):
        return self.index == 0 or card.strength >= self.strength or card.card_type == CardTypes.Shield


class Eagle(Card):  # Done

    def __init__(self):
        super().__init__(9, "Eagle", 2, False, False, CardTypes.Big_Bruiser, 3)

    def ability(self, game_state):
        if game_state.card_in_sky:
            return [[Board.kick_by_index, self.index]]
        else:
            return [[Board.fly, self.index]]

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


class Okapi(Card):  # Done

    def __init__(self):
        super().__init__(8, "Okapi", 3, True, True, CardTypes.Shield, 3)

    def ability(self, game_state):
        return [[Board.advance_by_index, self.index]]

    def stopping_condition(self, card):
        return card.strength >= self.strength

    def permanent_ability_interactional_trigger(self, card):
        return card.card_type == CardTypes.Big_Bruiser or card.card_type == CardTypes.Trampler


class Sloth(Card):

    def __init__(self):
        super().__init__(7, "Sloth", 2, False, False, CardTypes.Shield, 3)

    def ability(self, game_state):
        pass


class Panda(Card):

    def __init__(self):
        super().__init__(6, "Zen-Panda", 4, False, False, CardTypes.Little_Bully, 3)

    def ability(self, game_state):
        pass


class Coyote(Card):

    def __init__(self):
        super().__init__(5, "Coyote", 4, False, False, CardTypes.Little_Bully, 3)

    def ability(self, game_state):
        pass


class Weasel(Card):  # Done

    def __init__(self):
        super().__init__(4, "Weasel", 3, False, False, CardTypes.Undefined, 3)

    def ability(self, game_state):
        return [[Board.advance_to_front, self.index]]

    def stopping_condition(self, card):
        return card.strength <= self.strength


class Gazelle(Card):  # Done

    def __init__(self):
        super().__init__(3, "Gazelle", 2, False, True, CardTypes.Undefined, 3)

    def ability(self, game_state):
        return [[Board.overtake, self.index]]

    def permanent_ability_interactional_trigger(self, card):
        return card.card_type == CardTypes.Big_Bruiser

    def permanent_ability(self, card):
        return [[Board.enter_by_index, self.index]]


class Flamingo(Card):  # Done

    def __init__(self):
        super().__init__(2, "Flamingo", 4, False, False, CardTypes.Undefined, 3)

    def ability(self, game_state):
        if self.index > 1:
            return [[Board.switch_2_cards, self.index-2, self.index-1], [Board.overtake, self.index]]
        return []


class Armadillo(Card):

    def __init__(self):
        super().__init__(1, "Armadillo", 4, False, False, CardTypes.Little_Bully, 3)

    def ability(self, game_state):
        pass


class TasmanianDevil(Card):  # Done

    def __init__(self):
        super().__init__(0, "Tasmanian Devil", 2, False, False, CardTypes.Undefined, 3)

    def ability(self, game_state):
        indexes = []
        for card in game_state.jostling_cards:
            if card.id != self.id:
                indexes.append(card.index)

        random.shuffle(indexes)
        indexes.insert(0, self.index)

        return [[Board.reorder, indexes]]

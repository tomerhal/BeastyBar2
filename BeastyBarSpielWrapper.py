# Copyright 2019 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as python3
"""Kuhn Poker implemented in Python.

This is a simple demonstration of implementing a game in Python, featuring
chance and imperfect information.

Python games are significantly slower than C++, but it may still be suitable
for prototyping or for small games.

It is possible to run C++ algorithms on Python implemented games, This is likely
to have good performance if the algorithm simply extracts a game tree and then
works with that. It is likely to be poor if the algorithm relies on processing
and updating states as it goes, e.g. MCTS.
"""

import enum

import numpy as np

import pyspiel


class Action(enum.IntEnum):
    PASS = 0
    BET = 1


_NUM_PLAYERS = 2
_DECK = frozenset([0, 1, 2])
_GAME_TYPE = pyspiel.GameType(
    short_name="Beasty Bar",
    long_name="Beasty Bar",
    dynamics=pyspiel.GameType.Dynamics.SEQUENTIAL,
    chance_mode=pyspiel.GameType.ChanceMode.EXPLICIT_STOCHASTIC,
    information=pyspiel.GameType.Information.IMPERFECT_INFORMATION,
    utility=pyspiel.GameType.Utility.ZERO_SUM,
    reward_model=pyspiel.GameType.RewardModel.TERMINAL,
    max_num_players=_NUM_PLAYERS,
    min_num_players=_NUM_PLAYERS,
    provides_information_state_string=True,
    provides_information_state_tensor=True,
    provides_observation_string=True,
    provides_observation_tensor=True,
    provides_factored_observation_string=True)
_GAME_INFO = pyspiel.GameInfo(
    num_distinct_actions=len(Action),
    max_chance_outcomes=len(_DECK),
    num_players=_NUM_PLAYERS,
    min_utility=-2.0,
    max_utility=2.0,
    utility_sum=0.0,
    max_game_length=len(_DECK) * _NUM_PLAYERS)  # e.g. Pass, Bet, Bet


class KuhnPokerGame(pyspiel.Game):
    """A Python version of Kuhn poker."""

    def __init__(self, players, deck_len, params=None):
        super().__init__(_GAME_TYPE, _GAME_INFO, params or dict())
        self.players = players
        self.curr_player = random.choice(players)
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

    def new_initial_state(self):
        """Returns a state corresponding to the start of a game."""
        return KuhnPokerState(self)

    def make_py_observer(self, iig_obs_type=None, params=None):
        """Returns an object used for observing game state."""
        return KuhnPokerObserver(
            iig_obs_type or pyspiel.IIGObservationType(perfect_recall=False),
            params)


class KuhnPokerState(pyspiel.State):
    """A python version of the Kuhn poker state."""

    def __init__(self, game):
        """Constructor; should only be called by Game.new_initial_state."""
        super().__init__(game)
        self.cards = game.jostling_cards()
        self.bar = game.bar
        self.trash = game.trash
        self._game_over = False
        self._next_player = game.curr_player

    # OpenSpiel (PySpiel) API functions are below. This is the standard set that
    # should be implemented by every sequential-move game with chance.

    def current_player(self):
        """Returns id of the next player to move, or TERMINAL if game is over."""
        if self._game_over:
            return pyspiel.PlayerId.TERMINAL
        else:
            return self._next_player

    def _legal_actions(self, player):
        """Returns a list of legal actions, sorted in ascending order."""
        assert player >= 0
        if self.is_chance_node():
            return ["draw"]
        return game.legal_actions(player)

    def chance_outcomes(self):
        """Returns the possible chance outcomes and their probabilities."""
        assert self.is_chance_node()
        outcomes = sorted(self.game.deck_len-self._next_player.deck_len)
        p = 1.0 / len(outcomes)
        return [(o, p) for o in outcomes]

    def _apply_action(self, action):
        """Applies the specified action to the state."""
        self.game.apply_action(self._next_player,action)

    def _action_to_string(self, player, action):
        """Action -> string."""
        if player == pyspiel.PlayerId.CHANCE:
            return f"Deal:{action}"
        elif action == Action.PASS:
            return "Pass"
        else:
            return "Bet"

    def is_terminal(self):
        """Returns True if the game is over. ???????????we have max turn so is it good?"""
        return all(len(player.hand) == 0 for player in game.players)

    def returns(self):
        """Total reward for each player over the course of the game so far."""
        #todo idk what this is doing
        pot = self.pot
        winnings = float(min(pot))
        if not self._game_over:
            return [0., 0.]
        else:
            return game.scores

    def __str__(self):
        """String for debug purposes. No particular semantics are required."""
        return "".join([str(c) for c in self.cards] + ["pb"[b] for b in self.bets])


class KuhnPokerObserver:
    """Observer, conforming to the PyObserver interface (see observation.py)."""

    def __init__(self, iig_obs_type, params):
        """Initializes an empty observation tensor."""
        if params:
            raise ValueError(f"Observation parameters not supported; passed {params}")

        # Determine which observation pieces we want to include.
        pieces = [("player", 2, (2,))]
        if iig_obs_type.private_info == pyspiel.PrivateInfoType.SINGLE_PLAYER:
            pieces.append(("private_card", 3, (3,)))
        if iig_obs_type.public_info:
            if iig_obs_type.perfect_recall:
                pieces.append(("betting", 6, (3, 2)))
            else:
                pieces.append(("pot_contribution", 2, (2,)))

        # Build the single flat tensor.
        total_size = sum(size for name, size, shape in pieces)
        self.tensor = np.zeros(total_size, np.float32)

        # Build the named & reshaped views of the bits of the flat tensor.
        self.dict = {}
        index = 0
        for name, size, shape in pieces:
            self.dict[name] = self.tensor[index:index + size].reshape(shape)
            index += size

    def set_from(self, state, player):
        """Updates `tensor` and `dict` to reflect `state` from PoV of `player`."""
        self.tensor.fill(0)
        if "player" in self.dict:
            self.dict["player"][player] = 1
        if "private_card" in self.dict and len(state.cards) > player:
            self.dict["private_card"][state.cards[player]] = 1
        if "pot_contribution" in self.dict:
            self.dict["pot_contribution"][:] = state.pot
        if "betting" in self.dict:
            for turn, action in enumerate(state.bets):
                self.dict["betting"][turn, action] = 1

    def string_from(self, state, player):
        """Observation of `state` from the PoV of `player`, as a string."""
        pieces = []
        if "player" in self.dict:
            pieces.append(f"p{player}")
        if "private_card" in self.dict and len(state.cards) > player:
            pieces.append(f"card:{state.cards[player]}")
        if "pot_contribution" in self.dict:
            pieces.append(f"pot[{int(state.pot[0])} {int(state.pot[1])}]")
        if "betting" in self.dict and state.bets:
            pieces.append("".join("pb"[b] for b in state.bets))
        return " ".join(str(p) for p in pieces)


# Register the game with the OpenSpiel library

pyspiel.register_game(_GAME_TYPE, KuhnPokerGame)

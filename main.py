from board import Player, Game
from graphics import *
from cards import *
import random

deck1 = [Lion(), Hippo(), Crocodile(), Snake(), Giraffe(), Zebra(), Seal(), Chameleon(), Monkey(), Kangaroo(), Parrot(), Skunk()]
deck2 = [Lion(), Hippo(), Crocodile(), Snake(), Giraffe(), Zebra(), Seal(), Chameleon(), Monkey(), Kangaroo(), Parrot(), Skunk()]
deck3 = [Lion(), Hippo(), Crocodile(), Snake(), Giraffe(), Zebra(), Seal(), Chameleon(), Monkey(), Kangaroo(), Parrot(), Skunk()]
#deck2 = [Rhino(), Bear(), Tiger(), Cheetah(), Llama(), Porcupine(), Ostrich(), Penguin(), Dog(), Peacock(), Vulture(), Bat()]
#deck3 = [Elephant(), Camel(), Buffalo(), Eagle(), Okapi(), Sloth(), Panda(), Coyote(), Weasel(), Gazelle(), Flamingo(), Armadillo()]

testPlayer1 = Player('Nir1', Colors.Blue, deck1, CMDGraphics,seed=random.random())
testPlayer2 = Player('Nir2', Colors.Green, deck2, CMDGraphics,seed=random.random())
testPlayer3 = Player('Nir3', Colors.Red, deck3, CMDGraphics,seed=random.random())

# players = [testPlayer1, testPlayer2, testPlayer3, testPlayer4]
players = [testPlayer1, testPlayer2, testPlayer3]

board = Game(players, len(players[0].deck)+4)
# board = Board(players, 1)

#board.main_loop()

for i in range(100):
    deck1 = [Lion(), Hippo(), Crocodile(), Snake(), Giraffe(), Zebra(), Seal(), Chameleon(), Monkey(), Kangaroo(),
             Parrot(), Skunk()]
    deck2 = [Lion(), Hippo(), Crocodile(), Snake(), Giraffe(), Zebra(), Seal(), Chameleon(), Monkey(), Kangaroo(),
             Parrot(), Skunk()]
    deck3 = [Lion(), Hippo(), Crocodile(), Snake(), Giraffe(), Zebra(), Seal(), Chameleon(), Monkey(), Kangaroo(),
             Parrot(), Skunk()]
    testPlayer1 = Player('Nir1', Colors.Blue, deck1, CMDGraphics, seed=random.random())
    testPlayer2 = Player('Nir2', Colors.Green, deck2, CMDGraphics, seed=random.random())
    testPlayer3 = Player('Nir3', Colors.Red, deck3, CMDGraphics, seed=random.random())

    # players = [testPlayer1, testPlayer2, testPlayer3, testPlayer4]
    players = [testPlayer1, testPlayer2, testPlayer3]

    board = Game(players, len(players[0].deck) + 4)
    player = 0
    for turn in range(len(players)*(len(deck1)+4)):
        actions = board.legal_actions(players[player])
        print(board.legal_actions(players[player]))
        action = random.choice(actions)
        print("playing " + action)
        board.apply_action(players[player], action)
        player = (player + 1) % 3

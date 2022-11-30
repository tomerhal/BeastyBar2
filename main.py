from board import Player, Game
from graphics import *
from cards import *

deck1 = [Lion(), Hippo(), Crocodile(), Snake(), Giraffe(), Zebra(), Seal(), Chameleon(), Monkey(), Kangaroo(), Parrot(), Skunk()]
deck2 = [Rhino(), Bear(), Tiger(), Cheetah(), Llama(), Porcupine(), Ostrich(), Penguin(), Dog(), Peacock(), Vulture(), Bat()]
deck3 = [Elephant(), Camel(), Buffalo(), Eagle(), Okapi(), Sloth(), Panda(), Coyote(), Weasel(), Gazelle(), Flamingo(), Armadillo()]

testPlayer1 = Player('Nir1', Colors.Blue, deck1, CMDGraphics)
testPlayer2 = Player('Nir2', Colors.Green, deck2, CMDGraphics)
testPlayer3 = Player('Nir3', Colors.Red, deck3, CMDGraphics)

# players = [testPlayer1, testPlayer2, testPlayer3, testPlayer4]
players = [testPlayer1, testPlayer2, testPlayer3]

board = Game(players, len(players[0].deck)+4)
# board = Board(players, 1)

board.main_loop()

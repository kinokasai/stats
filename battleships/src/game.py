from grille import *
from helpers import *
from random import shuffle

class Player:
    def __init__(self):
        self.target = Grille.genere_grille()
        self.hitmap = Grille()

    def play():
        pass


class RandomPlayer(Player):
    def __init__(self):
        Player.__init__(self)

    def play(self):
        shots = 0
        stack = [to_dual(x) for x in range(100)]
        shuffle(stack)
        while self.target.any():
            self.target.shoot(stack.pop())
            shots += 1
        print(f"{shots} shots!")


if __name__ == '__main__':
    RandomPlayer().play()

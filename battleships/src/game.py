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
    def play(self):
        shots = 0
        stack = [to_dual(x) for x in range(100)]
        shuffle(stack)
        while self.target.any():
            self.target.shoot(stack.pop())
            shots += 1
        print(f"{shots} shots!")
        return shots

class HeuristicalPlayer(Player):
    def play(self):
        shots = 0
        stack = [to_dual(x) for x in range(100)]
        shuffle(stack)
        while self.target.any():
            pos = stack.pop()
            if self.target.shoot(pos):
                shots += self.target_play(pos)
        print(f"{shots} shots!")
        return shots

    def target_play(self, pos):
        stack = []
        add_to_stack(pos, stack)
        shots = 0
        while self.target.any() and stack:
            x, y = stack.pop()
            if x not in range(10) or y not in range(10):
                continue
            if self.target.shoot((x, y)):
                shots += self.target_play((x, y))
            shots += 1
        return shots

if __name__ == '__main__':
    HeuristicalPlayer().play()

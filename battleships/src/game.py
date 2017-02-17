from grille import *
from helpers import *
from random import shuffle
import pdb

class Player:
    def __init__(self):
        self.target = Grille.genere_grille()
        self.hitmap = Grille()

    def play():
        pass


def random_play(grid):
    shots = 0
    stack = [to_dual(x) for x in range(100)]
    shuffle(stack)
    while self.target.any():
        self.target.shoot(stack.pop())
        shots += 1
    return shots

def heuris_play(grid):
    target = grid
    shots = 0
    stack = [to_dual(x) for x in range(100)]
    shuffle(stack)
    while target.any():
        pos = stack.pop()
        hit, sunk = target.shoot(pos)
        if hit:
            shots += target_play(target, pos)
    return shots

def target_play(grid, pos):
    stack = []
    add_to_stack(pos, stack)
    shots = 0
    while grid.target.any() and stack:
        x, y = stack.pop()
        if x not in range(10) or y not in range(10):
            continue
        hit, sunk = self.target.shoot(pos)
        if hit:
            shots += self.target_play((x, y))
            shots += 1
    return shots



def pieces_on_case(grid, pos, boat):
    x, y = pos
    s = sum(grid.peut_placer(boat, (y, x-n), 'H')\
            for n in range(LONG[boat]))
    s += sum(grid.peut_placer(boat, (y-n, x), 'V')
             for n in range(LONG[boat]))
    return s

def propagate(hit_list, prob_map):
    prob_map = prob_map.reshape(10, 10)
    for x,y in hit_list:
        coeff = 40
        for i in range(1, 5):
            pos = (x+i, y)
            if prob_map.at(pos) == 0:
                break
            prob_map.set(pos, prob_map.at(pos) + coeff / abs(i))
        for i in range(1, 5):
            pos = (x, y+i)
            if prob_map.at(pos) == 0:
                break
            prob_map.set(pos, prob_map.at(pos) + coeff / abs(i))
        for i in range(-4, 0):
            pos = (x+i, y)
            if prob_map.at(pos) == 0:
                break
            prob_map.set(pos, prob_map.at(pos) + coeff / abs(i))
        for i in range(-4, 0):
            pos = (x, y+i)
            if prob_map.at(pos) == 0:
                break
            prob_map.set(pos, prob_map.at(pos) + coeff / abs(i))

def prob_play(target, hitmap=None):
    hitmap = hitmap or np.zeros(100).view(Grille).reshape(10, 10)
    boats = [i for i in range(1, 6)]
    probmap = np.zeros(100).view(Grille)
    shots = 0
    hit_list = []
    shot_list = []
    while boats:
        # We calculate the grid of probabilities
        probmap = np.array([np.sum([pieces_on_case(hitmap, (x, y), boat)\
                     for boat in boats])
              for x in range(10) for y in range(10)]).view(Grille)

        pos = to_dual(probmap.argsort()[-1])
        print(f'pos: {pos}')
        # value = probmap.at(pos)
        # print(f'value: {value}')
        # print(f'sort: {probmap.argsort()}')
        # print('probmap_b:\n', probmap)
        # shot_list.append(pos)
        # print(np.sum(pieces_on_case(hitmap, (0, 0), 5) for boat in boats))

        hit, slice = target.shoot(pos)
        if slice:
            print("is_ded")
            boats.remove(hit)
            probmap[slice] = 0
            hitmap[slice] = 0
        hitmap.set(pos, 1)
        # print('probmap_b:\n', probmap.reshape(10, 10))
        probmap.set(pos, 0)
        print('probmap_e:\n', probmap.reshape(10, 10))
        shots += 1
        # propagate(hit_list, probmap)

        print('hitmap:\n', hitmap)
        # print('target:\n', target)
        # print('shot_list:\n', shot_list)
        pdb.set_trace()
    return shots

if __name__ == '__main__':
    grid = Grille().genere_grille()
    print(f'{prob_play(grid)} shots!')

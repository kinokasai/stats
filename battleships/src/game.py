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
    boats = [i for i in range(1, 6)]
    shot = []
    while boats:
        pos = stack.pop()
        shot.append(pos)
        hit, sunk = target.shoot(pos)
        if hit:
            shots += target_play(target, pos, boats, shot)
    return shots

def target_play(target, pos, boats, shot):
    stack = []
    add_to_stack(pos, stack)
    shots = 0
    while boats and stack:
        print(stack)
        x, y = stack.pop()
        shot.append((x, y))
        if x not in range(10) or y not in range(10) or (x, y) in shot:
            continue
        hit, sunk = target.shoot((x, y))
        print(sunk)
        if sunk:
            boats.remove(hit)
        if hit in boats:
            print('hit', hit)
            shots += target_play(target, (x, y), boats, shot)
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
    for x,y in hit_list:
        propagate_dir(prob_map, (x, y), range(1, 5), (lambda i: (x+i, y)))
        propagate_dir(prob_map, (x, y), range(1, 5), (lambda i: (x, y+i)))
        propagate_dir(prob_map, (x, y), range(-4, 0), (lambda i: (x+i, y)))
        propagate_dir(prob_map, (x, y), range(-4, 0), (lambda i: (x, y+i)))

def propagate_dir(pmap, pos, range_obj, lmda):
    coeff = 40
    for i in range_obj:
        pos = lmda(i)
        value_at = grid_get(pmap, pos)
        if not value_at:
            break
        value = value_at + int(coeff / abs(i))
        grid_set(pmap, pos, value)

def grid_set(l, pos, value):
    x, y = pos
    if x in range(10) and y in range(10):
        l[x][y] = value

def grid_get(l, pos):
    x, y = pos
    try:
        return l[x][y]
    except IndexError:
        return 0

def max_index(l):
    max = -1
    maxi, maxj = (0, 0)
    for i in range(10):
        for j in range(10):
            if l[i][j] > max:
                max = l[i][j]
                maxi, maxj = i, j
    return maxi, maxj

def set_slice(l, slice, value):
    for i, j in slice:
        l[i][j] = 0

def print_grid(l):
    for i in range(10):
        for j in range(10):
            print(l[i][j], end=' ')
        print()

def prob_play(target, hitmap=None):
    hitmap = hitmap or np.zeros(100).view(Grille).reshape(10, 10)
    boats = [i for i in range(1, 6)]
    shots = 0
    hit_list = []
    shot_list = []
    while boats and target.any():
        # We calculate the grid of probabilities
        probmap = [[np.sum([pieces_on_case(hitmap, (x, y), boat)\
                     for boat in boats]) for x in range(10)] for y in range(10)]

        propagate(hit_list, probmap)
        pos = max_index(probmap)
        x, y = pos
        # print(f'pos: {pos}')

        # print('probmap_b:')
        # print_grid(probmap)

        hit, slice = target.shoot(pos)
        if hit:
            hit_list.append(pos)
            if slice:
                boats.remove(hit)
                set_slice(hitmap, slice, 1)
                [hit_list.remove(i) for i in slice]
        else:
            hitmap[x][y] = 1
        probmap[x][y] = 0
        shots += 1

        if shots >= 100:
            print("Something weird happened")
            break
    return shots

if __name__ == '__main__':
    grid = Grille().genere_grille()
    print(f'{prob_play(grid)} shots!')

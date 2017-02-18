import numpy as np
from numpy.random import randint
from random import choice
from functools import reduce
import matplotlib.pyplot as plt
import pdb

# Longueurs des bateaux
LONG = {
    1: 5, # Porte-avions
    2: 4, # Croiseur
    3: 3, # Contre-torpilleurs
    4: 3, # Sous-marin
    5: 2, # Torpilleur
}

# Valeurs des directions
DIR = {
    'V': (1,0), # Vertical
    'H': (0,1), # Horizontal
}

class Grille(np.ndarray):
    def __init__(self):
        self.boats = {}
        self.shot = []

    def __new__(cls, taille=(10,10)):
        return np.zeros(taille).view(cls)

    def slice_index(self, bateau, position, direction):
        j1, i1 = position
        j2, i2 = np.array(position) + np.array(DIR[direction]) * LONG[bateau]
        lj = [j1] * LONG[bateau] if j1 == j2 else list(range(j1,j2))
        li = [i1] * LONG[bateau] if i1 == i2 else list(range(i1,i2))
        for i, j in zip(lj, li):
            if i < 0 or j < 0:
                raise IndexError
        return [lj,li]

    def cases(self, bateau, position, direction):
        return self[self.slice_index(bateau, position, direction)]

    # This fucking takes a (y, x)!
    def peut_placer(self, bateau, position, direction):
        try:
            cases = self.cases(bateau, position, direction)
            return (cases == 0).all()
        except IndexError:
            return False

    def place(self, bateau, position, direction):
        if self.peut_placer(bateau, position, direction):
            slice = self.slice_index(bateau, position, direction)
            boat = np.array([bateau] * LONG[bateau]).reshape(self[slice].shape)
            l = []
            for i in zip(slice[0], slice[1]):
                l.append(i)
            self.boats[bateau] = l
            self[slice] = boat
            return self
        else:
            return None

    def place_alea(self, bateau):
        h, w = self.shape
        while self.place(bateau, (randint(h),randint(w)), choice(list(DIR.keys()))) is None:
            pass

    def at(self, pos):
        if self.shape != (10, 10):
            self = self.reshape(10, 10)
        x, y = pos
        if x not in range(10) or y not in range(10):
            return 0
        return self[y][x]

    def set(self, pos, value):
        if self.shape != (10, 10):
            self = self.reshape(10, 10)
        x, y = pos
        if x in range(10) and y in range(10):
            self[y][x] = value

    def affiche(self):
        plt.imshow(self, interpolation='nearest')

    def neighbors(self, pos):
        x, y = pos
        l = []
        l.append(self.at((x + 1, y)))
        l.append(self.at((x - 1, y)))
        l.append(self.at((x, y + 1)))
        l.append(self.at((x, y - 1)))
        return l

    # This returns a tuple saying if a boat hase been sunk.
    # (1, 3) -> hit sunk third boat
    # (0, -1) -> miss
    # (1, -1) -> hit, nothing sunk
    def shoot(self, position):
        y, x = position
        position = x, y
        boat_type = self.at(position)
        self.set(position, 0)
        neigh = self.neighbors(position)
        slice = None
        if boat_type not in self.ravel():
            slice = self.boats[boat_type]
        return (boat_type, slice)

    @staticmethod
    def eq(grilleA, grilleB):
        return (grilleA == grilleB).all()

    @staticmethod
    def genere_grille():
        grille = Grille()
        for bateau in LONG.keys():
            grille.place_alea(bateau)
        return grille

if __name__ == '__main__':
    G = Grille.genere_grille()
    G.affiche()
    plt.show()

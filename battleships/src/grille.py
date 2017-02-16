import numpy as np
from numpy.random import randint
from random import choice
from functools import reduce
import matplotlib.pyplot as plt

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
    def __new__(cls, taille=(10,10)):
        return np.zeros(taille).view(cls)

    def slice_index(self, bateau, position, direction):
        j1, i1 = position
        j2, i2 = np.array(position) + np.array(DIR[direction]) * LONG[bateau]
        lj = [j1] * LONG[bateau] if j1 == j2 else list(range(j1,j2))
        li = [i1] * LONG[bateau] if i1 == i2 else list(range(i1,i2))
        return [lj,li]

    def cases(self, bateau, position, direction):
        return self[self.slice_index(bateau, position, direction)]

    def peut_placer(self, bateau, position, direction):
        try:
            return (self.cases(bateau, position, direction) == 0).all()
        except IndexError:
            return False

    def place(self, bateau, position, direction):
        if self.peut_placer(bateau, position, direction):
            i = self.slice_index(bateau, position, direction)
            self[i] = np.array([bateau] * LONG[bateau]).reshape(self[i].shape)
            return self
        else:
            return None

    def place_alea(self, bateau):
        h, w = self.shape
        while self.place(bateau, (randint(h),randint(w)), choice(list(DIR.keys()))) is None:
            pass

    def affiche(self):
        plt.imshow(self, interpolation='nearest')

    def shoot(self, position):
        x, y = position
        if self[x][y]:
            self[x][y] = 0
            return True
        return False

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

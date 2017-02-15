from grille import *
from functools import reduce

def positions(grille):
    xi = [np.arange(n) for n in grille.shape]
    return np.stack(np.meshgrid(*xi), 2).reshape(-1,2)

def nb_placements_bateau(bateau, grille):
    return np.sum(grille.peut_placer(bateau, position, direction) \
            for position in positions(grille) \
            for direction in DIR.keys())

def nb_placements_liste_bateaux(bateaux, grille):
    # Cas de base
    if len(bateaux) == 0:
        return 1
    # Récursion
    nb_placements = 0
    for position in positions(grille):
        for direction in DIR.keys():
            # On essaie de placer le bateau
            g = grille.copy().place(bateaux[0], position, direction)
            # Si on a réussi
            if g is not None:
                # On ajoute le nombre de placements possibles des bateaux restants
                nb_placements += nb_placements_liste_bateaux(bateaux[1:], g)
    return nb_placements

def trouve_grille_alea(grille):
    n = 0
    trouve = False
    while not trouve:
        g = Grille.genere_grille()
        trouve = Grille.eq(g, grille)
        n += 1
    return n

def nb_approx_placements_liste_bateaux(bateaux, grille):
    N = [nb_placements_bateau(b, grille) for b in bateaux]
    return reduce(lambda a,b: a*b, N)

if __name__ == '__main__':
    G = Grille()
    # print(nb_placements_bateau(1, G))
    print(nb_placements_liste_bateaux([1,2,3], G))
    # print(nb_approx_placements_liste_bateaux([1,2], G))

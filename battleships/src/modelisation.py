from grille import *
from combinatoire import *

from scipy.signal import savgol_filter
from scipy.stats import binom
import random

fact = np.math.factorial
def C(k,n):
    return fact(n) / (fact(k) * fact(n-k))

def aleatoire(grille):
    jeu = Grille()
    cases_restantes = [tuple(pos) for pos in positions(jeu)]
    nb_coups = 0
    touches = 0
    while touches < 17:
        coup = random.choice(cases_restantes)
        if jeu[coup] == 0:
            if grille[coup] != 0:
                jeu[coup] = 2
                touches += 1
            else:
                jeu[coup] = 1
            cases_restantes.remove(coup)
            nb_coups += 1
    return nb_coups

def dist_theorique_aleatoire():
    X = []
    P = []
    tmp = 0
    nb_jeux_total = C(17,100)
    for x in range(17,101):
        nb_jeux_en_x_coups = C(17,x)
        p = (nb_jeux_en_x_coups - tmp) / nb_jeux_total
        tmp = nb_jeux_en_x_coups
        X.append(x)
        P.append(p)
    return (X,P)

def distribution(modelisation, N):
    dist = {}
    G = Grille.genere_grille()
    for i in range(N):
        n = modelisation(G)
        if n not in dist.keys():
            dist[n] = 1/N
        else:
            dist[n] += 1/N
    return tuple(zip(*sorted(dist.items())))

def esperance(dist):
    X,P = dist
    return np.sum(np.array(X) * np.array(P))

if __name__ == '__main__':
    dist_theo = dist_theorique_aleatoire()
    dist_exp = distribution(aleatoire, 1000)
    print("Espérance théorique:", esperance(dist_theo))
    print("Espérance expérimentale:", esperance(dist_exp))
    x, y = dist_theo
    plt.plot(x, y, label='théorique')
    x, y = dist_exp
    plt.plot(x, y, label='expérimentale')
    plt.legend()
    plt.show()

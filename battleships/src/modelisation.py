from grille import *
from combinatoire import *
from game import *

from scipy.signal import savgol_filter
from scipy.stats import binom
import random

fact = np.math.factorial
def C(k,n):
    return fact(n) / (fact(k) * fact(n-k))

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
    grid = Grille.genere_grille()
    for i in range(N):
        n = modelisation(grid)
        n = 0
        print(modelisation())
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
    dist_exp = distribution(HeuristicalPlayer().play, 1000)
    x, y = dist_exp
    plt.plot(x, y, label='expérimentale')
    plt.legend()
    plt.show()
    plt.savefig("lol.png")

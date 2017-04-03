from sys import path
path.append('.')

from nanowebs import creeNanoWeb1
from internautes import *


# Création du SimpleWeb
nanoweb = creeNanoWeb1()

# Bob se ballade dans le nanoweb
bob = Internaute(nanoweb)

# Bob est dans le noeud 3
bob.goTo(3)

# Bob conserve les valeurs de epsilon
# toutes les 100 itérations
# dans ce fichier
bob.trace(100, "epsilons_v1.txt")

# Bob se ballade 10000 fois
# ou jusqu'à epsilon < 0.01
bob.walk(10000, 0.01)

# Bob affiche la fréquence de sa présence
# dans chaque noeud durant sa promenade
bob.showFrequencies()


fred = InternauteV2(nanoweb)
fred.trace(100, "epsilons_v2.txt")
fred.walk(10000, 0.01)

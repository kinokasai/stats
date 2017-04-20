from sys import path
path.append('.')

import matplotlib.pyplot as plt

from nanowebs import *
from internautes import *
from utils import grid_axes

nanowebs = [creeNanoWeb1(), creeNanoWeb2(), creeNanoWeb3()]
N = 10000
epsilon = 0.01
interval = 1
init_state = 1

i = 0
for nanoweb in nanowebs:
    i += 1

    bob = Internaute(nanoweb)
    bob.goTo(init_state)
    bob.trace(interval, 'logs/epsilons_internaute_{}.txt'.format(i))
    bob.walk(N, epsilon)

    fred = Kolmogogol(nanoweb)
    fred.trace(interval, 'logs/epsilons_kolmogogol_{}.txt'.format(i))
    # fred.trace(interval, 'logs/epsilons_kolmogogol_uniform_{}.txt'.format(i))
    init = np.zeros(fred.web.n)
    init[init_state] = 1
    # init = np.ones(fred.ord) / fred.ord
    fred.walk(N, epsilon, init)

    print()

for i in range(len(nanowebs)):
    with open('logs/epsilons_internaute_{}.txt'.format(i+1), 'r') as log:
        epsilons = [float(line) for line in log]
        plt.step(np.arange(len(epsilons)), epsilons, label='nanoweb {}'.format(i+1))
plt.xlim((0,100))
plt.xlabel('Pas de temps ($t$)')
plt.ylabel('Convergence ($\epsilon$)')
plt.legend()
plt.savefig('doc/img/epsilons_internaute_t{}.png'.format(interval))

plt.clf()

for i in range(len(nanowebs)):
    with open('logs/epsilons_kolmogogol_{}.txt'.format(i+1), 'r') as log:
    # with open('logs/epsilons_kolmogogol_uniform_{}.txt'.format(i+1), 'r') as log:
        epsilons = [float(line) for line in log]
        plt.step(np.arange(len(epsilons)), epsilons, label='nanoweb {}'.format(i+1))
plt.xlim((0,100))
plt.xlabel('Pas de temps ($t$)')
plt.ylabel('Convergence ($\epsilon$)')
plt.legend()
plt.savefig('doc/img/epsilons_kolmogogol_t{}.png'.format(interval))
# plt.savefig('doc/img/epsilons_kolmogogol_uniform_t{}.png'.format(interval))

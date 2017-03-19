from scipy.stats import poisson
from simul import *
from genoseq import *


def check_poisson(n, p):
    if not (n >= 100 and n*p <= 10):
        raise ValueError("Cannot approximate with a Poisson law with these parameters: n=%d, p=%f" % (n, p))
    return n*p


def exp_prob_dists(words, model, l):
    k = len(words[0])
    n = l-k+1
    dists = []
    for w in words:
        p = prob(stnl(w), model)
        lambda_ = check_poisson(n, p)
        dist = [poisson.pmf(x, lambda_) for x in range(l-k+2)]
        dists.append(np.array(dist))
    return np.array(dists)


def exp_prob_ge(words, model, l, x):
    k = len(words[0])
    n = l-k+1
    ge = []
    for w in words:
        p = prob(stnl(w), model)
        lambda_ = check_poisson(n, p)
        ge.append(poisson.pmf(x, lambda_) + poisson.sf(x, lambda_))
    return np.array(ge)

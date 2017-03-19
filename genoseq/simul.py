from fixation import *
from utils import grid_axes


def simul(len, model=(0.25,0.25,0.25,0.25), N=1000):
    return [simul_seq(len, model) for n in range(N)]


def counts_list(words, sim):
    k = len(words[0])
    idx = [encode(w, k) for w in words]
    cl = [np.array(count_words(seq, k)) for seq in sim]
    return np.array(cl)[:,idx]


def emp_counts(counts_list):
    return np.apply_along_axis(np.mean, 0, counts_list)


def emp_prob_ge(counts_list, n):
    ge = (counts_list >= n).astype(int)
    return np.apply_along_axis(np.sum, 0, ge) / len(counts_list)


def emp_prob_dists(counts_list, k, l):
    eq = [(counts_list == n).astype(int) for n in range(l-k+1)]
    freqs = [np.apply_along_axis(np.sum, 0, eq_n) / len(counts_list) for eq_n in eq]
    return np.array(freqs).T


def plot_exp_emp_counts(exp_counts, emp_counts):
    x = np.arange(len(exp_counts))
    plt.plot(x, emp_counts, label="Observé")
    plt.plot(x, exp_counts, label="Attendu")
    plt.xlabel("Indice lexicographique")
    plt.ylabel("Nombre d'occurrences moyen")
    plt.ylim((0, 5))
    plt.legend()


def plot_prob_dists(words, dists):
    _, ax = plt.subplots()

    dists = [dist[np.logical_not(np.isclose(dist, 0))] for dist in dists]
    N = [len(dist) for dist in dists]
    K = len(dists)
    
    inds = [np.arange(n) for n in N]
    width = 1 / (K*1.5)

    cmap = plt.cm.get_cmap("Set3", K+1)
    
    bars = []
    labels = []
    i = 0
    for word, dist in zip(words, dists):
        pos = inds[i] - (width * K / 2) + (i * width)
        bars.append(ax.bar(pos, dist[:N[i]], width, color=cmap(i)))
        labels.append(word)
        i += 1
    
    xt = np.array(inds[N.index(max(N))])
    ax.set_xticks(xt - width/2)
    ax.set_xticklabels(xt)
    ax.legend(bars, labels, loc='upper center')

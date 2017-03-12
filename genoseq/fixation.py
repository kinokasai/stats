from genoseq import *
import matplotlib.pyplot as plt
import math


def nlists(size):
    xi = [np.arange(4)] * size
    cart_prod = np.array(np.meshgrid(*xi, indexing='ij')).T.reshape(-1, len(xi))
    nlists = np.swapaxes(np.swapaxes(cart_prod, 0, 1)[::-1], 0, 1)
    return nlists.tolist()


def encode(word, size):
    return np.sum(ctn(char) * 4 ** i for char, i in zip(word, range(size - 1, -1, -1)))


def decode(idx, size):
    l = []
    for size in range(size - 1, -1, -1):
        l.append(idx // 4**size)
        idx %= 4 ** size
    return l


def count_words(nlist, size):
    counts = np.zeros(4**size)
    for i in range(len(nlist) - size + 1):
        w = nlist[i:i+size]
        counts[encode(nlts(w), size)] += 1
    return counts.tolist()


def expected_counts(nlist, size):
    freqs = freq_letters(nlist)
    counts = []
    for w in nlists(size):
        n = count_letters(w)
        count = np.prod([freqs[a]**n[a] for a in range(4)]) * (len(nlist) - size + 1)
        counts.append(count)
    return counts


def plot_counts(nlists, sizes):
    """
    nlists -- dict in the form {nlist_label: nlist}
    sizes -- list of word sizes
    """
    grid_size = math.ceil(math.sqrt(len(sizes)))
    axes = []
    for i in range(len(sizes)):
        y = i // grid_size
        x = i % grid_size
        axes.append(plt.subplot2grid((grid_size, grid_size), (y, x)))

    for i in range(len(sizes)):
        count_max = 0
        for label, nlist in nlists.items():
            exp = expected_counts(nlist, sizes[i])
            obs = count_words(nlist, sizes[i])
            axes[i].scatter(exp, obs, s=50, label=label, marker=".")
            # axes[i].plot(np.arange(len(obs)), obs, label=label)
            max_ = max(exp)
            if max_ > count_max:
                count_max = max_

        id_ = [0, count_max]
        axes[i].plot(id_, id_, color="red", linewidth=1)

        # axes[i].set_xlabel("Indice lexicographique")
        axes[i].set_xlabel("Nombre d'occurrences attendu")
        axes[i].set_ylabel("Nombre d'occurrences observé")
        axes[i].set_title("k = " + str(sizes[i]))
        axes[i].legend()

    plt.gcf().suptitle("Nombres d'occurrences des mots de taille k dans le génome de S. cerevisae")

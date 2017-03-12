from genoseq import *
from functools import reduce


def nlists(k):
    xi = [np.arange(4)] * k
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
    dict = {}
    for i in range(len(nlist) - size + 1):
        seq = nlts(nlist[i:i+size])
        try:
            dict[seq] += 1
        except KeyError:
            dict[seq] = 1
    return dict


def expected_counts(freqs, k, l):
    counts = []
    for w in nlists(k):
        n = count_letters(w)
        count = reduce(lambda x, y: x*y, [freqs[a]**n[a] for a in range(4)]) * (l-k+1)
        counts.append(count)
    return counts

from genoseq import *


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

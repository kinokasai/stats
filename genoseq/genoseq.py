import numpy as np

ctn_dict = {
    'A': 0,
    'C': 1,
    'G': 2,
    'T': 3,
}

ntc_dict = {
    0: 'A',
    1: 'C',
    2: 'G',
    3: 'T',
}


def ctn(char):
    try:
        return ctn_dict[char]
    except KeyError:
        return -1


def ntc(n):
    try:
        return ntc_dict[n]
    except KeyError:
        return '_'


def stnl(s):
    return [ctn(char) for char in s]


def read_fasta(file_name):
    file = open(file_name)
    lines = [line.rstrip('\n') for line in file if line[0] != '>']
    acids = [[ctn(char) for char in line] for line in lines]
    file.close()
    return acids


def count_letters(nlist):
    cnt = np.zeros(4, dtype=np.int)
    for n in nlist:
        cnt[n] += 1
    return tuple(cnt)


def freq_letters(nlist):
    tpl = count_letters(nlist)
    l = [n / sum(tpl) for n in tpl]
    return tuple(l)


def logprob(nlist, model):
    return np.sum(np.log(model[n]) for n in nlist)


def flogprob(tpl, model):
    return np.sum(np.log(model[j]) for j in range(4) for _ in range(tpl[j]))


def simul_seq(len, model):
    l = []
    cum_model = (model[0], model[0] + model[1], model[0] + model[1] + model[2],
                 model[0] + model[1] + model[2] + model[3])
    for n in np.random.ranf(len):
        for i in range(4):
            if n < cum_model[i]:
                l.append(i)
                break
    return l

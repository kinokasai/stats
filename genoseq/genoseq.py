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
        return ctn_dict[char.upper()]
    except KeyError:
        return -1


def ntc(n):
    try:
        return ntc_dict[n]
    except KeyError:
        return '_'


def stnl(s):
    return [ctn(char) for char in s]


def nlts(nl):
    return ''.join([ntc(n) for n in nl])


def read_fasta(file_name):
    file = open(file_name)
    lines = [line.rstrip('\n') for line in file if line[0] not in ['>',';']]
    acids = [[ctn(char) for char in line] for line in lines]
    seq = []
    for s in acids:
        seq += s
    file.close()
    return seq


def count_letters(nlist):
    cnt = np.zeros(4, dtype=np.int)
    for n in nlist:
        if n == -1: continue
        cnt[n] += 1
    return tuple(cnt)


def freq_letters(nlist):
    return tuple(np.array(count_letters(nlist)) / len(nlist))


def logprob(nlist, model):
    return np.sum(np.log(model[n]) for n in nlist)


def flogprob(tpl, model):
    prob = 0.
    for a in range(4):
        pa = np.log(model[a])
        prob += pa * tpl[a]
    return prob


def prob(nlist, model):
    tpl = count_letters(nlist)
    return np.exp(flogprob(tpl, model))


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

import random
import os
from KLC.settings import BASE_DIR


def get_lst():
    lst = []
    with open(os.path.join(BASE_DIR, "data/luogu.txt"), "r", encoding='utf-8') as f:
        con = f.read()
        name = con.split(',')
        for i in name:
            if i != '':
                lst.append(i)

    with open(os.path.join(BASE_DIR, "data/cf.txt"), "r", encoding='utf-8') as f:
        con = f.read()
        name = con.split(',')
        for i in name:
            if i != '':
                lst.append(i)

    with open(os.path.join(BASE_DIR, "data/at.txt"), "r", encoding='utf-8') as f:
        con = f.read()
        name = con.split(',')
        for i in name:
            if i != '':
                lst.append(i)

    return lst


def get_prob():
    return random.choice(get_lst())


def get_probs(n):
    return random.sample(get_lst(), n)


def write_prob(n):
    prob = get_probs(n)

    with open(os.path.join(BASE_DIR, "data/prob.txt"), "w", encoding='utf-8') as f:
        for i in prob:
            f.write(i)
            f.write('\n')


def get_list(n):
    lst = []
    with open(os.path.join(BASE_DIR, "data/prob.txt"), "r", encoding='utf-8') as f:
        for i in range(n):
            lst.append(f.readline()[:-1])
    return lst

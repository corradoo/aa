import random

def dsa(n, q, B=1000):
    a = 0
    h = 0
    while(a <= B and h <= B):
        if random.random() < q:
            a += 1
        else:
            h += 1

        if h >= n and a >= h:  # Attacker get to honest after n blocks
            return True

        if a == n and h <= n:  # Attacker mined n block before honest
            return True

    return a > h


def mca(n, q, t, B=1000):
    num_successful_attacks = 0
    for i in range(t):
        if i % 1000 == 0:
            print(f'n{n} q{q} t{i}')
        if dsa(n, q, B):
            num_successful_attacks += 1
    return num_successful_attacks / t

from hashlib import sha256, sha512, sha1, md5, shake_128
from struct import unpack
import math
import mmh3
from matplotlib import pyplot as plt

alphas = {
    3: 0.62560871093725783198500641115,
    4: 0.67310202386766599233548265739,
    5: 0.69712263380102416804875375530,
    6: 0.70920845287002329682833053248,
    7: 0.71527118996133942147695553096,
    8: 0.71830763819181383227618018595,
    9: 0.71982714782040011202713737966,
    10: 0.72058722597645269495707971678,
    11: 0.72096734613621909810824869710,
    12: 0.72115742651737845487667069838
}


def generate_sets(n=10000):
    M = []
    b = 1
    for i in range(1, n+1):
        M.append([str(k) for k in range(b, b+i)])
        b += i
    return M


def get_hash(h, m):
    b = m.encode(encoding="utf-8")
    return unpack('L', h(b).digest()[:8])[0] >> 32


def get_leftmost_bit_position(b, w):
    return 32-b+1 - w.bit_length()


def calc_alpha(m):
    if m == 5:
        return 0.69712263380102416804875375530
    else:
        return 0.7213 / (1 + 1.079 / m)


def hyper_log_log(b, h, S):
    m = 2**b
    M = [0] * m

    # cnt = 0
    for v in S:
        x = get_hash(h, v)
        j = x & (m - 1)
        w = x >> b
        M[j] = max(M[j], get_leftmost_bit_position(b, w))
        # if cnt % 10**2 == 0:
        #     print(M[:10])
        # cnt+=1

    Z = 1/(sum([2**-m for m in M]))
    alpha = alphas[b]
    E = alpha*m*m*Z
    if E <= 2.5 * m:
        V = M.count(0)
        if V != 0:
            E = m * math.log(m / V)
    elif E > 1/30 * 2 ** 64:
        E = -2 ** 64 * math.log(1 - E / 2 ** 64)
    return int(E)


def get_hash_m(h, m):
    b = m.encode(encoding="utf-8")
    return float(unpack('L', h(b).digest()[:8])[0]) / 2**64


def min_count(k, h, M):
    T = [1.0 for _ in range(k)]
    for m in M:
        hashed = get_hash_m(h, m)
        if(hashed < T[-1]):
            T[-1] = hashed
            T.sort()
    estimate = 0
    if T[-1] == 1:  # n < k case
        estimate = sum(1 for n in T if n != 1.0)
    else:
        estimate = (k-1)/T[-1]
    return estimate


def exp_b():
    M = generate_sets(10000)
    outcome = {}
    for b in range(3, 12+1):
        print(b)
        outcome[b] = []

        for i in range(0, 10000, 10):
            est = hyper_log_log(b, md5, M[i])
            outcome[b].append((len(M[i]), est/len(M[i])))

    # print(outcome)

    for b in range(3, 12+1):
        plt.plot([x[0] for x in outcome[b]], [x[1] for x in outcome[b]], '.')
        plt.grid()
        plt.title(f'b={b}')
        plt.xlabel('n')
        plt.ylabel('n^ / n')
        plt.savefig(f'md5/est_{b}b.png')
        plt.clf()


def test():
    card = 10**5
    S = [str(i) for i in range(card)]
    E = hyper_log_log(10, sha256, S)
    print(f'b={10} -> {E}\tE/n:{abs((E-card)/card)*100}%')


def comparison():
    M = generate_sets(10000)
    outcome = {}

    for b in range(3, 12+1):
        outcome[b] = []
        for i in range(100, 10000, 10):
            print(i)
            k = 2**b*5//32
            est = hyper_log_log(b, sha256, M[i])
            est_m = min_count(k, sha256, M[i])
            outcome[b].append((len(M[i]), est/len(M[i]), est_m/len(M[i])))
            # outcome_m[b].append((len(M[i]),est/len(M[i])))

    for b in range(3, 12+1):
        plt.plot([x[0] for x in outcome[b]], [x[1] for x in outcome[b]], '.')
        plt.plot([x[0] for x in outcome[b]], [x[2] for x in outcome[b]], '.')
        plt.grid()
        plt.title(f'b={b} k={2**b*5//32}')
        plt.xlabel('n')
        plt.ylabel('n^ / n')
        plt.savefig(f'comp_{b}b_{2**b*5//32}k.png')
        plt.clf()


# comparison()
exp_b()

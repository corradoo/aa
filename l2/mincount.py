from zlib import crc32
from hashlib import sha256, sha512, sha1, md5, shake_128
from struct import unpack
from random import randint
from matplotlib import pyplot as plt
import math

hash_weak = lambda x: int(shake_128(x.encode(encoding="utf-8")).hexdigest(1), 16) / 2**8

def f_k(x: float, k):
    return math.exp(x * k) * pow((1.0 - x), k)

def chernoff(delta,k):
    eps1 = delta/(1+delta)
    eps2 = delta/(1-delta)
    return f_k(eps1,k) + f_k(-eps2,k)

def get_chernoff(alpha = 0.05, k = 400, eps=10**-6):
    a = 0.0
    b = 1.0
    while (a <= b - eps):
        c = (a + b) / 2
        if chernoff(c,k) > alpha:
            a = c
        else:
            b = c
    return a

def bytes_to_float(b):
    return float(crc32(b) & 0xffffffff) / 2**32

# def bytes_to_float(b):
#     return float(unpack('L', sha256(b).digest()[:8])[0]) / 2**64


def str_to_float(s, encoding="utf-8"):
    return bytes_to_float(s.encode(encoding))


def get_hash_m(h, m):
    b = m.encode(encoding="utf-8")
    return float(unpack('L', h(b).digest()[:8])[0]) / 2**64


def min_count(k, h, M):
    T = [1.0 for _ in range(k)]
    for m in M:
        hashed = 1.0
        if h == None:
            hashed = hash_weak(m)
        else:
            hashed = get_hash(h, m)
        if(hashed < T[-1]):
            T[-1] = hashed
            T.sort()
    estimate = 0
    if T[-1] == 1:  # n < k case
        estimate = sum(1 for n in T if n != 1.0)
    else:
        estimate = (k-1)/T[-1]
    return estimate


n = 1000


def hash_test():
    samples = 10000
    n = 200
    k = 100
    errs = [0, 0, 0, 0,0]

    for s in range(samples):
        print(s)
        M = [f'{randint(0,0xffffffff)}' for _ in range(n)]

        errs[0] += min_count(k, sha1, M)/n
        errs[1] += min_count(k, sha256, M)/n
        errs[2] += min_count(k, sha512, M)/n
        errs[3] += min_count(k, md5, M)/n
        errs[4] += min_count(k, None, M)/n

    for i in range(len(errs)):
        errs[i] /= samples
        errs[i] = abs(errs[i] - 1)*100

    print(f'n={n} k={k} samples={samples}\t{errs}')
# 10000 100                          [0.509817489454889, 0.2836142868489211, 0.09047242105533204, 0.1761872319924196]
# 1000 100                           [0.3979754905900412, 0.3707452826272717, 0.018031429062770332, 0.5022772140451215]
#                                    [0.04337106848735228, 0.03317794954696973, 0.04120423424428532, 0.042950162466826036]
# n=1000 k=400 samples=20000         [0.005596782547567791, 0.00841719548155817, 0.004734899817993021, 0.008403940377521568]
# n=1000 k=400 samples=20000         [0.003925929116321836, 0.02566107403441098, 0.010011500784701255, 0.005626348629328426]
# n=1000 k=400 samples=5000          [0.0036202441719090928, 0.011162275316944914, 0.05360310867073004, 0.051621449081729054]
# n=1000 k=10 samples=5000           [0.1575561721415042, 0.3860394393933708, 0.7101746689686994, 0.6422032449758364]
# n=1000 k=10 samples=5000           [0.4394515071830418, 0.14645582540681046, 0.08330581016817717, 0.3881742677318556]
# n=1000 k=3 samples=5000            [2.59911785035154, 1.044050885723391, 0.35967155540368445, 1.8815164545450624]
# n=1000 k=3 samples=5000            [0.3553671265190239, 2.471576369846784, 0.9938972459413886, 0.5487184312827909]
# n=200 k=100 samples=10000          [0.0033294112141590837, 0.019631354499982656, 0.08380907734050203, 0.06078613059190552]
# n=200 k=100 samples=10000          [0.031791442830919614, 0.06336998077078881, 0.06394455359159945, 0.12348874250803776, 0.26671023059472443]


def simple():
    ks = [2, 3, 10, 100, 400]
    xs = []
    ys = []
    for k in ks:
        err = []
        x = []
        y = []
        for n in range(1, 10001):
            print(n)
            # Table of hashes
            M = [1.0 for _ in range(k)]
            for _ in range(1, n+1):
                h = str_to_float(f'{randint(0,0xffffffff)}')
                if(h < M[-1]):
                    M[-1] = h
                    M.sort()
            estimate = 0
            if M[-1] == 1:  # n < k case
                estimate = sum(1 for n in M if n != 1.0)
            else:
                estimate = (k-1)/M[-1]
            x.append(n)
            y.append(estimate/n)
            err.append(abs(estimate/n-1.0))
            # print(f'Estimate={estimate}')
        xs.append(x)
        ys.append(y)
        print(
            f'For k={k} Less than 10 %: {sum(1 for e in err if e < 0.1)/len(x)}')

    id = 0
    for k in ks:
        plt.plot(xs[id], ys[id], '.')
        plt.grid()
        plt.title(f'k={k}')
        plt.xlabel('n')
        plt.ylabel('n^ / n')
        plt.savefig(f'est_{k}k.png')
        plt.clf()
        id += 1


def generate_multiset(n=10000):
    M = []
    b = 1
    for i in range(1, n+1):
        M.append([str(k) for k in range(b, b+i)])
        b += i
    return M


def find_k():
    n = 10000
    a = 0
    b = 400
    eps = 0.001
    goal = 0.95
    curr = 0
    M = generate_multiset()

    while(abs(curr/n-goal) > eps and a+1 != b):
        k = (a+b)//2
        print(f'a={a}, b={b}, k={(a+b)//2}')
        curr = 0
        for s in M:
            if(abs(min_count(k, sha1, s)/len(s)-1) < 0.1):
                curr += 1
        print(curr/n)
        if(curr/n < goal):
            a = k
        else:
            b = k


def zad7():
    n = 10000
    M = generate_multiset(n)
    k = 400
    ests = []
    abss = []
    x = []
    for s in M:
        x.append(len(s))
        ratio = min_count(k, sha1, s)/len(s)
        ests.append(ratio)
        abss.append(abs(ratio-1))

    abss.sort()
    alphas = [0.05, 0.01, 0.005]
    for alpha in alphas:
        delta_id = int((1-alpha)*len(abss))
        delta = abss[delta_id]
        
        czebyszew = math.sqrt((n-k+1)/(n*alpha*(k-2)))
        chernoff = get_chernoff(alpha=alpha)
        
        plt.plot(x, ests, '.')
        plt.hlines(y=[1-delta, 1+delta], xmin=0, xmax=n,
                   colors='red', linestyles='--', lw=1, label='1+-delta')
        plt.hlines(y=[1-czebyszew, 1+czebyszew], xmin=0, xmax=n,
                   colors='purple', linestyles='--', lw=1, label='Czebyszew')
        plt.hlines(y=[1-chernoff, 1+chernoff], xmin=0, xmax=n,
                   colors='orange', linestyles='--', lw=1, label='Chernoff')
        plt.grid()
        plt.title(f'k={k} alpha={alpha*100}% delta={delta}')
        plt.xlabel('n')
        plt.ylabel('n^ / n')
        plt.legend()
        plt.savefig(f'delta_{alpha}_cc.png')
        plt.clf()


# simple()
# generate_multiset()
# find_k()
# hash_test()
zad7()

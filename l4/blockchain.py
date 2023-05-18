import math
import numpy as np
import matplotlib.pyplot as plt
from attack import mca2

ns = [1, 3, 6, 12, 24, 48]

def grunspan(p, q, n): return 1 - \
    sum([(p**n * q**k - q**n*p**k) * math.comb(k+n-1, k) for k in range(0, n)])


def nakamoto(p, q, n): return 1 - sum([math.exp(-(n*q/p))*(
    (n*q/p)**k/math.factorial(k)) * (1-(q/p)**(n-k)) for k in range(0, n)])


def ex1_1():

    qs = np.linspace(0.0, 0.5, 500)

    grun = [[grunspan(1-q, q, n) for q in qs] for n in ns]
    naka = [[nakamoto(1-q, q, n) for q in qs] for n in ns]

    # Plot the Grunspan results
    for index, n in enumerate(ns):
        plt.plot(qs, grun[index], label=str(f'n={n}'))
    plt.xlabel('q')
    plt.ylabel('Probability')
    plt.title('Plot of Grunspan')
    plt.legend()
    plt.grid()
    plt.savefig("grun.png")
    plt.clf()

    # Plot the Nakamoto results
    for index, n in enumerate(ns):
        plt.plot(qs, naka[index], label=str(f'n={n}'))
    plt.xlabel('q')
    plt.ylabel('Probability')
    plt.title('Plot of Nakamoto')
    plt.legend()
    plt.grid()
    plt.savefig("naka.png")
    plt.clf()

    # Plot comparisons
    for index, n in enumerate(ns):
        plt.plot(qs, naka[index], label=str(f'Nakamoto'))
        plt.plot(qs, grun[index], label=str(f'Grunspan'))
        plt.xlabel('q')
        plt.ylabel('Probability')
        plt.title(f'Comparison n={n}')
        plt.legend()
        plt.grid()
        plt.savefig(f"out/comp{n}.png")
        plt.clf()

def find_n(q, goal, f, m=120):
    for n in range(1,m):
        if f(1-q,q,n) <= goal:
            return n
    return m

def ex1_2():
    qs = np.linspace(0.01, 0.49, 50)
    goals = [0.1,0.01,0.001]
    outcome_g = [[find_n(q,g,grunspan) for q in qs] for g in goals]
    outcome_n = [[find_n(q,g,nakamoto) for q in qs] for g in goals]

    for index, g in enumerate(goals):
        name = str(g*100)
        plt.plot(qs, outcome_g[index], '.',label="Grunspan's")
        plt.plot(qs, outcome_n[index], '.', label="Nakamoto")
        plt.xlabel('q')
        plt.ylabel('n')
        plt.title(f'Probability={name}%')
        plt.grid()
        plt.legend()
        plt.savefig(f"2p{name}.png")
        plt.clf()

def ex2(n=12,t=1000, s=50,B=1000):
    qs = np.linspace(0.3, 0.5, s)
    gs = [grunspan(1-q, q, n) for q in qs]
    naks = [nakamoto(1-q, q, n) for q in qs]
    mc = [mca2(n,q,t,B) for q in qs]
    plt.plot(qs, gs, '.', label="Grunspan's")
    plt.plot(qs, naks, '.', label="Nakamoto")
    plt.plot(qs, mc, 'x', label="Monte Carlo")
    plt.xlabel('q')
    plt.ylabel('Prob')
    plt.title(f'Double spending attack(n={n})')
    plt.grid()
    plt.legend()
    plt.savefig(f"out/3mc{n}_B{B}_t{t}_s{s}.png")
    plt.clf()

ex1_1()
for n in ns:
    ex2(n)
    # ex2(n,s=100)
    # ex2(n,B=10000)
    # ex2(n,t=10000)
# ex1_2()
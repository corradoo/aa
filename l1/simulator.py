from random import seed
from random import random
import math

def scenario2(n : int = 10000):

    prob = 1/n
    rounds = 0
    slotCnt = 0
    leader = -1

    while True:
        rounds += 1
        slotCnt = 0
        for i in range(n):
            if random() < prob:
                slotCnt += 1
                leader = i
        if slotCnt == 1:
            break

    # print(f'S2:\tLeader #{leader} chosen in round(slot) {rounds}')
    return rounds
    
def scenario3(u: int = 1000, n : int = 500):
    L = math.ceil(math.log2(u))+1
    
    rounds = 0
    slotInRound = 0
    slotCnt = 0
    leader = -1

    search = True
    while search:
        rounds += 1
        slotInRound = 0
        #round
        for i in range(1,L+1):
            slotCnt = 0
            prob = 1/2**i
            slotInRound +=1
            #slot
            for node in range(n):
                if random() < prob:
                    slotCnt += 1
                    leader = node
            if slotCnt == 1:
                search = False
                break 

    # print(f'S3:\tLeader #{leader} chosen in round {rounds}, slot {L*rounds+slotInRound}')
    return L*(rounds-1)+slotInRound, rounds

def zad1():
    scenario2()
    scenario3()

from matplotlib import pyplot as plt

def histogram():
    binwidth = 1
    u=1000
    s2 = []
    s3_1 = []
    s3_2 = []
    s3_3 = []
    for _ in range(1000):
        s2.append(scenario2())
        s3_1.append(scenario3(u,2)[0])
        s3_2.append(scenario3(u,u//2)[0])
        s3_3.append(scenario3(u,u)[0])
    plt.hist(s2,bins=range(min(s2), max(s2) + binwidth, binwidth))
    plt.xticks(range(min(s2), max(s2)+1))
    plt.savefig('s2.png')

    import numpy as np
    rounds_begin = range(1, 200, math.ceil(math.log2(u)))
    plt.clf()
    plt.title('n=2')
    plt.hist(s3_1,bins=range(min(s3_1), max(s3_1) + binwidth, binwidth))
    plt.vlines(x=range(1, max(s3_1), math.ceil(math.log2(u)+1)),ymin=0,ymax=200, colors='r', ls='--', lw=0.5, label='round begin')
    plt.savefig('s3_1.png')

    plt.clf()
    plt.title('n=u/2')
    plt.hist(s3_2,bins=range(min(s3_2), max(s3_2) + binwidth, binwidth))
    plt.vlines(x=range(1, max(s3_3), math.ceil(math.log2(u)+1)),ymin=0,ymax=200, colors='r', ls='--', lw=0.5, label='round begin')
    plt.savefig('s3_2.png')

    plt.clf()
    plt.title('n=u')
    plt.hist(s3_3,bins=range(min(s3_3), max(s3_3) + binwidth, binwidth))
    plt.vlines(x=range(1, max(s3_3), math.ceil(math.log2(u)+1)),ymin=0,ymax=200, colors='r', ls='--', lw=0.5, label='round begin')
    plt.savefig('s3_3.png')

from statistics import mean, variance, stdev

def zad3():
    s2 = []
    for _ in range(10000):
        s2.append(scenario2())
    print(f'3)\tE:{mean(s2)} Var:{variance(s2)}')

def zad4(u,n):
    samples = 100
    sum_rounds = 0
    r1_cnt = 0
    for _ in range(samples):
        _,r = scenario3(u,n)
        sum_rounds += r
        if r == 1:
            r1_cnt += 1
    return sum_rounds/samples, r1_cnt/samples


def plot4():
    u=1024
    y = []
    for n in range(2,u):
        print(n)
        y.append(zad4(u,n)[1])
    plt.clf()
    plt.title('Zad4')
    plt.plot(y)
    plt.grid()
    plt.savefig('plot4_1.png') 


# histogram()
# zad3()
# print(f'4)\tProbability to get leader in 1 round(u=1000 n=2):\t{zad4(1000,2)[1]} ')
# print(f'4)\tProbability to get leader in 1 round(u=1000 n=u/2):\t{zad4(1000,500)[1]} ')
# print(f'4)\tProbability to get leader in 1 round(u=n=1000):\t\t{zad4(1000,1000)[1]} ')
plot4()
import itertools
import random


lookup = {}


def round(regs, order, i):
    n = len(regs)
    random.shuffle(order)
    if i == 0:
        print(f"{regs}")

    for o in order:
        if o == 0:
            if regs[-1] == regs[0]:
                regs[0] = (regs[0] + 1) % (n + 1)
        else:
            if regs[o] != regs[o - 1]:
                regs[o] = regs[o - 1]

    if verify(regs):
        print(f"\033[92m{regs}\033[0m round:{i}")
        return True

    return False


def verify(regs):
    val = regs[0]
    cnt = 1
    for r in regs:
        if r != val:
            val = r
            cnt += 1
        if cnt > 2:
            # print(regs)
            return False
    # print(f'\033[92m{regs}\033[0m')
    return True


def path(regs, step: int = 0):
    n = len(regs)
    m = step
    if regs in lookup:
        return step + lookup[regs]

    if verify(regs):
        lookup[regs] = 0
        return step

    regs = list(regs)
    # First proc
    if regs[0] == regs[-1]:
        # print(f'\033[94m{regs[0]}\033[0m{regs[1:]}')
        # regs[0] = (regs[0]+ 1) % (n+1)
        m = max(m, path(tuple([(regs[0] + 1) % (n + 1)] + regs[1:]), step + 1))

    # Other procs
    for id, r in enumerate(regs[1:]):
        if regs[id] != regs[id + 1]:
            # print(f'{regs[:id+1]}\033[96m{regs[id+1]}\033[0m{regs[id+2:]}')
            # regs[id+1] = regs[id]
            m = max(
                m, path(tuple(regs[: id + 1] + [regs[id]] + regs[id + 2 :]), step + 1)
            )

    lookup[tuple(regs)] = m - step
    return m


def find_max(n:int):
    x = [i for i in range(n + 1)]
    perms = [p for p in itertools.product(x, repeat=n)]

    m = 0
    mp = 0
    for it, p in enumerate(perms):
        if it % 10000 == 0:
            print(f"Dict size: {len(lookup)}")
        m = max(m, path(p))
        if mp != m:
            print(f"{p} -> max ={m}")
        mp = m
    print(m)

find_max(7)
p9 = (0, 7, 6, 5, 4, 3, 2, 1,0)
p10 = (0, 8, 7, 6, 5, 4, 3, 2, 1,0)
p11 = (0, 9,8, 7, 6, 5, 4, 3, 2, 1,0)
p12 = (0, 10, 9,8, 7, 6, 5, 4, 3, 2, 1,0)
p13 = (0, 11,10, 9,8, 7, 6, 5, 4, 3, 2, 1,0)

# lookup = {}
# print(f"9 -> {path(p9)}")
# lookup = {}
# print(f"10 -> {path(p10)}")
# lookup = {}
# print(f"11 -> {path(p11)}")
# lookup = {}
# print(f"13 -> {path(p13)}")

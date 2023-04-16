from hashlib import sha256, sha512, sha1, md5, shake_128
from struct import unpack
import math

def get_hash(h, m):
    b = m.encode(encoding="utf-8")
    return unpack('L', h(b).digest()[:8])[0] >> 32

def get_leftmost_bit_position(w):
    return  23 - w.bit_length()


def hyper_log_log(b, h, S):

    m = 2**b
    # breakpoint()
    M = [0] * m

    cnt = 0
    for v in S:
        # breakpoint()
        x = get_hash(h,v)
        # j = 1 + int(x[:b],2)
        # w = int(x[b:],2)
        j = x & (m - 1)
        w = x >> b
        M[j] = max(M[j], get_leftmost_bit_position(w))
        # print(f'x:{x} -> {bin(x)}')
        # print(f'j:{j} -> {bin(j)}')
        # print(f'w:{w} -> {bin(w)} ')
        if cnt % 10**5 == 0: 
            print(M[:10])
        cnt+=1

        # breakpoint()

    
    Z = 1/(sum([2**-m for m in M]))

    alpha = 0.7213 / (1 + 1.079 / m)

    E = alpha*m*m*Z

    # if E <= 2.5 * m:
    #     V = M.count(0)
    #     if V != 0:
    #         E = m * math.log(m / V)
    # elif E > 1/30 * 2 ** 32:
    #     E = -2 ** 32 * math.log(1 - E / 2 ** 32)
    return int(E)

card = 10**8
S = [ str(i) for i in range(card)]

E = hyper_log_log(10,sha256,S)
print(f'{E} E/n:{abs((E-card)/E)*100}%')

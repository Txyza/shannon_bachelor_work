import gmpy2
from gmpy2 import *
import datetime
import time as t
time = int(datetime.datetime.now().strftime('%Y%m%d%I%M%S'))
state = random_state(time)


def generate_random_p(p):
    return gmpy2.mpz_random(state, p)


def generate_p_b_q():
    q = generate_random_p(2**256)
    b = generate_random_p(2**768)
    while not is_prime(b * q + 1):
        q = gmpy2.next_prime(q)
        b = generate_random_p(2**768)
    p = b * q + 1
    return p, b, q


def generate_g(p, b, q):
    t = 2
    g = gmpy2.powmod(t, b, p)
    res = gmpy2.powmod(g, q, p)
    while res != 1 and g != 1:
        t += 1
        g = gmpy2.powmod(t, b, p)
        res = gmpy2.powmod(g, q, p)
    return g


def generate_x(p):
    return gmpy2.mpz_random(state, p)


def time_powmod(func, a, b, c, d):
    res = None
    start = t.clock()
    for i in range(100):
        res = func(a, b, c)
    end = t.clock()
    print(d, ' -> \t\t\t%.8f' % ((end - start) / 100))
    return res


if __name__ == "__main__":
    p, b, q = generate_p_b_q()
    g = generate_g(p, b, q)

    a1 = generate_x(q)
    b1 = generate_x(q)

    A = time_powmod(gmpy2.powmod, g, a1, p, 'A')
    B = time_powmod(gmpy2.powmod, g, b1, p, 'B')
    x = generate_random_p(p)
    y = generate_random_p(p)

    X = time_powmod(gmpy2.powmod, g, x, p, 'X')
    Y = time_powmod(gmpy2.powmod, g, y, p, 'Y')

    l = 128
    d = 2**l + time_powmod(gmpy2.powmod, X, 1, 2**l, 'd')
    e = 2**l + time_powmod(gmpy2.powmod, Y, 1, 2**l, 'e')
    Sa_step = time_powmod(gmpy2.powmod, x + d * a1, 1, q, 'Sa_step')
    Sa = time_powmod(gmpy2.powmod,
                     Y * gmpy2.powmod(B, e, p),
                     Sa_step,
                     p,
                     'Sa')

    Sb_step = time_powmod(gmpy2.powmod, y + e * b1, 1, q, 'Sb_step')
    Sb = time_powmod(gmpy2.powmod,
                     X * gmpy2.powmod(A, d, p),
                     Sb_step,
                     p,
                     'Sb')
    print("""
    p = {}
    q = {}
    g = {}
    a1 = {}
    b1 = {}
    A = {}
    B = {}
    x = {}
    X = {}
    y = {}
    Y = {}
    d = {}
    e = {}
    Sa = {}
    Sb = {}
    """.format(p, q, g, a1, b1, A, B, x, X, y, Y, d, e, Sa, Sb))

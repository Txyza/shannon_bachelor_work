import gmpy2
from gmpy2 import *
import datetime
import time as t
import random
import os
time = int(datetime.datetime.now().strftime('%Y%m%d%I%M%S'))
state = random_state(time)


def powmod(a, step, mod):
        b = 1
        while step:
            if (step & 1) == 1:
                step -= 1
                b = (b * a) % mod
            step >>= 1
            a = (a * a) % mod
        return b % mod


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


def time_code(func, a, d):
    res = None
    start = t.clock()
    for i in range(1):
        res = func(a)
    end = t.clock()
    print(d, ' -> \t\t\t%.8f' % ((end - start) / 1))
    return res


def time_powmod(func, a, b, c, d):
    res = None
    start = t.clock()
    for i in range(1):
        res = func(a, b, c)
    end = t.clock()
    # print(d, ' -> \t\t\t%.8f' % ((end - start) / 100))
    return res


def selection(generate_key):
    random.seed(generate_key)
    file_list = os.listdir("helper/key")
    N = random.randint(4, 11)
    answer = list()
    for i in range(N):
        answer.append("helper/key/%s" % random.choice(file_list))
    return answer


def generate_code_key(code_files):
    text_files = list()
    for file in code_files:
        f = open(file, 'rb')
        text_files.append(bytearray(f.read()))
        f.close()
    answer = text_files[0]
    for i in range(1, len(text_files)):
        answer = xor(answer, text_files[i])
    return answer


def xor(answer, text):
    for i in range(len(answer)):
        answer[i] = answer[i] ^ text[i % 1024]
    return answer


def encode_file(code_key):
    file_code = 'test1'
    res_file = open('1%s' % file_code, 'wb')
    with open(file_code, 'rb') as f:
        while True:
            text = f.read(1024)
            if text == b'':
                break
            text = bytearray(text)
            text = xor(text, code_key)
            res_file.write(text)
    res_file.close()


def decode_file(code_key):
    file_code = '1test1'
    res_file = open('2%s' % file_code, 'wb')
    with open(file_code, 'rb') as f:
        while True:
            text = f.read(1024)
            if text == b'':
                break
            text = bytearray(text)
            text = xor(text, code_key)
            res_file.write(text)
    res_file.close()


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
    '''
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
    '''
    files = selection(Sb)
    print(files)
    key = generate_code_key(files)
    print(key)
    time_code(encode_file, key, 'encode_file')
    time_code(decode_file, key, 'decode_file')
    #encode_file(key)
    #decode_file(key)

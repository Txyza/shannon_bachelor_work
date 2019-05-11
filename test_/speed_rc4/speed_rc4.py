from helper.src.rc4 import encrypt
from src.protocol.src.shannon import Shannon
from string import ascii_lowercase, ascii_uppercase, digits
from random import choice
from time import perf_counter

# Название тестируемого файла
file_in = 'test2'

alphabet = ascii_uppercase + ascii_lowercase + digits
key = ''.join([choice(alphabet) for _ in range(10000)])


def encode_file_rc4():
    global file_in
    global key
    # key = 'Very long and confidential key' * 100
    with open(file_in, 'rb') as f:
        while True:
            text = f.read()
            if text == b'':
                break
            encrypt(text.decode('latin-1'), key)


def encode_file_shannon():
    global file_in
    Shannon().encode(None, file_in)


def time_code(func, d):
    res = None
    start = perf_counter()
    for i in range(1):
        res = func()
    end = perf_counter()
    print(d, ' ->  %.8f' % ((end - start) / 1))
    return res


time_code(encode_file_rc4, 'RC4 encode')
time_code(encode_file_shannon, 'Shannon encode')

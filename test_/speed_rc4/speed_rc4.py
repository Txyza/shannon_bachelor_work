from helper.src.rc4 import encrypt
from src.protocol.src.shannon import Shannon
import time as t

# Название тестируемого файла
file_in = 'test1'


def encode_file_rc4():
    global file_in
    key = 'Very long and confidential key' * 100
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
    start = t.perf_counter()
    for i in range(1):
        res = func()
    end = t.perf_counter()
    print(d, ' ->  %.8f' % ((end - start) / 1))
    return res


time_code(encode_file_rc4, 'RC4 encode')
time_code(encode_file_shannon, 'Shannon encode')

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from helper.rc4 import decrypt, encrypt
import time as t


def encode_file():
    file_code = 'test2'
    res_file = open('1%s' % file_code, 'wb')
    key = 'Very long and confidential key' * 10
    # print(decrypt(encrypted, key))
    with open(file_code, 'rb') as f:
        while True:
            text = f.read()
            if text == b'':
                break
            text = encrypt(text.decode('latin-1'), key)
            res_file.write(text)


def time_code(func, d):
    res = None
    start = t.clock()
    for i in range(1):
        res = func()
    end = t.clock()
    print(d, ' -> \t\t\t%.8f' % ((end - start) / 1))
    return res


time_code(encode_file, 'encode_file')
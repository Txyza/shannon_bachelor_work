# -*- coding: utf-8 -*-
import random, base64
from hashlib import sha1


def crypt(data, key): 
    x = 0
    box = list(range(256))
    for i in range(256):
        try:
            x = (x + box[i] + key[i % len(key)]) % 256
        except:
            pass
        box[i], box[x] = box[x], box[i]
    x = y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(char ^ box[(box[x] + box[y]) % 256]))
 
    return ''.join(out)

 
def encrypt(data, key, encode=base64.b64encode, salt_length=16): 
    salt = ''
    for n in range(salt_length):
        salt += chr(random.randrange(256))
    data = salt + crypt(data, sha1((key + salt).encode()).digest())
    #if encode:
    #    data = encode(data)
    return data.encode()


def decrypt(data, key, decode=base64.b64decode, salt_length=16):
    if decode:
        data = decode(data)
    salt = data[:salt_length]
    return crypt(data[salt_length:], sha1(key + salt).digest())


filepath = 'test1'
originalf = open(filepath, "rb")
file = originalf.read()
originalf.close()
destpath = 'test21'
key = 'heryertdsfgsertset'
data = encrypt(file, key)
dest = open(destpath, "wb")
dest.write(data)
dest.close()
exit()

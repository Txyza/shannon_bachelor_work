# ==============
#      Date: 04.12.2016
#       Author: Chusovitin Anton Romanovich
# ==============


import os
import hashlib
import random

def rename():

    for name in os.listdir("text/"):
        newName = hashlib.md5()
        newName.update(name.encode())
        os.rename("text/"+name, "textCode/"+newName.hexdigest()+".txt")


def delsimbol():
    for name in os.listdir("textCode/"):
        print(name)
        file = open("textCode/{}".format(name), "r", encoding="latin-1")
        TEXT = file.read()
        #print(TEXT)
        file.close()
        file = open("textCode/{}".format(name), "w", encoding="utf-8")
        a1 = ""
        for text in TEXT:
            if ord(text) < 1104:
                a1 += text
            else:
                print(text, ' -> ', ord(text))
        file.write(a1)
        file.close()


def delete_space():
    for name in os.listdir("textCode/"):
        with open("textCode/{}".format(name), "rb") as f:
            text = bytearray(f.read())
        with open("textCode/{}".format(name), "wb") as f:
            f.write(text[300::])


def generation():
    for i in range(1, 301):
        s = bytearray(random.randint(0, 255) for j in range(0, 200000))
        with open('backups/generation/{}'.format(i), 'wb') as f:
            f.write(s)
            print('write {}'.format(i))


def del_size():
    for name in os.listdir("textCode/"):
       if os.path.getsize('textCode/{}'.format(name)) < 100000:
           os.remove('textCode/{}'.format(name))


if __name__ == '__main__':
    a = input('Input')
    if a == '1':
        rename()
        delete_space()
        del_size()
    elif a == '2':
        delete_space()
    elif a == '3':
        generation()
    elif a == '4':
        del_size()
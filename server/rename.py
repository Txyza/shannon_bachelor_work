# ==============
#      Date: 04.12.2016
#       Author: Chusovitin Anton Romanovich
# ==============


import os
import hashlib

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

if __name__ == '__main__':
    rename()
    #delsimbol()
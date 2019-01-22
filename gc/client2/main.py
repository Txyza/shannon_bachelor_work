#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==============
#      Date: 01.12.2016
#       Author: Chusovitin Anton Romanovich
# ==============

import socket
import random
import os
import time
import base64


def generationKey(server):
    P = int(server.recv(1024).decode())
    G = int(server.recv(1024).decode())
    Ya = int(server.recv(1024).decode())
    Xb = random.randint(0, (2 ** 128) - 1)
    Yb = powmod(G, Xb, P)
    server.send(str(Yb).encode())
    print("P == ", P)
    print("G == ", G)
    print("Ya == ", Ya)
    print("Yb == ", Yb)
    print("Z == ", powmod(Ya, Xb, P))
    return powmod(Ya, Xb, P)

def powmod(a, step, mod):
    b = 1
    while step:
        if (step & 1) == 1:
            step -= 1
            b = (b * a) % mod
        step >>= 1
        a = (a * a) % mod
    return b % mod

def downloadFiles(server, raund):
    time.sleep(1)
    server.send("210450".encode("utf-8"))                   # Необходимая длина шифр-текста
    data = ""
    for i in range(0, 128):
        print(i)
        file2 = open("raunds/{}/{}.txt".format(raund, i), 'w')
        file = open("text/"+str(i)+".txt", "w", encoding="latin-1")
        while True:
            data = server.recv(262144*2).decode("latin-1")
            if data == "next":
                break
            else:
                file2.write(data)
                file.write(data)
            if not data:
                break
        file2.close()
        file.close()

def sendMessage(server, text1):
    time.sleep(1)
    for text in range(1,2):
        file = open("message.txt", "r")
        time.sleep(0.2)
        lenText = os.path.getsize("message.txt")
        line = file.read(16384)
        inlen = 16384
        while line:
            time.sleep(0.2)
            server.send(line.encode("utf-8"))
            if(inlen > lenText): break
            time.sleep(0.2)
            line = file.read(16384)
            inlen += 16384
        file.close()
        server.send("next".encode("utf-8"))
        time.sleep(0.5)


def sendFiles(server):
    for text in range(0,128):
        file = open("text/" + str(text)+ ".txt", "r")
        time.sleep(0.2)
        line = file.read(131072)
        lenText = os.path.getsize("text/" + str(text) + ".txt")
        print(text, "  size = ", lenText)
        inlen = 131072
        line = line.encode()
        server.send(line)
        time.sleep(0.3)
        while line:
                # print(line)
                # line = base64.b64encode(line)#.encode("utf-8"))
                # print("text = ", line)
                #print("yep")

                line = file.read(131072)
                inlen += 131072
                line = line.encode()
                server.send(line)
                time.sleep(0.3)
        if lenText <= inlen:
            print(text, "  next")
            server.send("next".encode())
            time.sleep(0.3)
        file.close()


def deltext():
    list = os.listdir(path=".\\text")
    for text in list:
        os.remove("text\\"+text)
    return list


def bits(n):
    ans = []
    sum1 = 0
    for i in range(0, 128):
        a = bit(n, i)
        if a == 1:
            sum1 += 1
        ans.append(a)
    return ans


def bit(num, pos):
    return (num & (1 << pos)) >> pos

"""
def xorText(list):
    file = open("1.txt", "r")
    text1 = file.read()
    for i in list:
        if i == 1:
            file2 = open("text/" + str(i) + ".txt", "r")
            text2 = file2.read()
            file2.close()
            text1 = xor(text1, text2)
    text1 = base64.b64encode(text1.encode())
    file2 = open("message.txt", "w")
    file2.write(text1.decode())
    file2.close()
    file.close()
    return text1
"""

def xorTest(text1, list):
    #text1 = text1.decode()
    #print(text1)
    fl = 0
    #text1 = text1.split()

    for i in range(0, 128):
        if list[i] == 1:
            fl += 1
            file2 = open("text/" + str(i) + ".txt", "rb")
            text2 = bytearray(file2.read())
            file2.close()
            text1 = xor(text1, text2)
            if fl == 55:
                break
    return text1


def xorMessage(list, message):
    fl = 0
    for i in range(0, 128):
        if list[i] == 1:
            file2 = open("text/" + str(i) + ".txt", "rb")
            text2 = bytearray(file2.read())
            file2.close()
            message = xor(message, text2)
    return message


def xor(text1, text2):
    lenText2 = len(text2)
    j = 0
    for i in range(len(text1)):
        text1[i] = text1[i] ^ text2[j]
        j += 1
        if j == lenText2-1:
            j = 0
    return text1


def dow(server, raund):
    data = ""
    for i in range(0, 128):
        print(i)
        file2 = open("raunds/{}/{}.txt".format(raund, i), 'wb')
        file = open("text/" + str(i) + ".txt", "wb")
        data = server.recv(1024).decode()
        with open('../server/textCode/{}'.format(data), 'rb') as f:
            f.seek(random.randint(500, 80000))
            data = f.read(402401)
            file2.write(data)
            file.write(data)
        file2.close()
        file.close()


if __name__ == '__main__':
    '''            2 КЛИЕНТУ        '''
    '''
    print("next".encode())
    HOST, PORT = "127.0.0.1", 1338
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))
    Z = generationKey(server)
    ans = bits(Z)
    text1 = xorText(ans)
    sendMessage(server, text1)  # Клиенту
    sendFiles(server)
    #deltext()
    server.close()
    '''
    for i in range(0, 300):
        HOST, PORT = "127.0.0.1", 1337
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((HOST, PORT))
        Z = generationKey(server)
        list_bits = bits(Z)
        os.mkdir("raunds/{}".format(i))
        with open('test_/statistic.txt', 'a') as f:
            f.write('{}\n'.format(sum(list_bits)))
        with open('raunds/{}/stat.txt'.format(i), 'w') as f:
            ch = 0
            for b in list_bits:
                if b == 1:
                    f.write('{} '.format(ch))
                ch += 1
        clock1 = time.time()
        dow(server, i)
        #downloadFiles(server, i)
        clock2 = time.time()
        with open('time_download', 'a') as f:
            f.write('{}) {}\n'.format(i, clock2 - clock1))
        server.close()
        for name in os.listdir("files/"):
            with open("files/{0}".format(name), "rb") as f:
                text_message = bytearray(f.read())
            # Шифрование исходного
            clock1 = time.time()
            text1 = xorTest(text_message, list_bits)
            clock2 = time.time()
            with open('time_xor', 'a') as f:
                f.write('{}) {} -> {}\n'.format(i, name, clock2-clock1))
            with open('test_/{0}_{1}'.format(i, name), 'wb') as f:
                f.write(text1)
                print("{}_{} encode success".format(i, name))
            with open('test_/{0}_{1}'.format(i, name), 'rb') as f:
                #for text in text1:
                text1 = bytearray(f.read())
            # Шифрование шифртекста
            #text1 = xorTest(text1, list_bits)
            #with open('success/{0}_{1}'.format(i, name), 'wb') as f:
                #f.write(sl)
            #    f.write(text1)
                #for text in text1:
                #    f.write(text)
            #    print("{}_{} decode success".format(i, name))
            #print(text1)

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

def downloadFiles(server):
    time.sleep(1)
    server.send("210450".encode("utf-8"))                   # Необходимая длина шифр-текста
    data = ""
    for i in range(0, 128):
        print(i)
        file = open("text/"+str(i)+".txt", "w")
        while True:
            data = server.recv(262144*2).decode("utf-8")
            if data == "next":
                break
            else:
                #print(data)
                #data = base64.b64decode(data)
                #print(data.decode())
                file.write(data)
            if not data:
                break
        file.close()
        #print(data)

def sendMessage(server, text1):
    time.sleep(1)
    for text in range(1,2):
        file = open("message.txt", "r")
        time.sleep(0.2)
        lenText = os.path.getsize("message.txt")
        line = file.read(16384)
        inlen = 16384
        while line:
            time.sleep(0.1)
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
        print(text)
        file = open("text/" + str(text)+ ".txt", "r")
        time.sleep(0.2)
        line = file.read(10240)
        lenText = os.path.getsize("text/" + str(text) + ".txt")
        print("size = ", lenText)
        #inlen = 131072
        while line:
            #print(line)
            server.send(line.encode("utf-8"))
            time.sleep(0.5)
            line = file.read(10240)
            #inlen += 131072
            #print(lenText, " -> ", inlen)
        server.send("next".encode("utf-8"))
        time.sleep(0.5)
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

def xor(text1, text2):
    lenText2 = len(text2)
    j = 0
    ans = ""
    for i in text1:
        ans += chr(ord(i) ^ (ord(text2[j])))
        j+=1
        if j == lenText2-1:
            j = 0
    return ans

if __name__ == '__main__':
    '''         Получение с сервера тексты и xor     '''
    HOST, PORT = "127.0.0.1", 1337
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))
    Z = generationKey(server)
    downloadFiles(server)
    server.close()
    '''            2 КЛИЕНТУ        '''
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
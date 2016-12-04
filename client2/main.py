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
    server.send("21045".encode("utf-8"))                   # Необходимая длина шифр-текста
    data = ""
    for i in range(128):
        filename = server.recv(2048).decode()
        #print(filename)
        file = open("text/"+str(i)+".txt", "w")
        while True:
            data = server.recv(2048).decode("utf-8")
            if data == "next":
                break
            else:
                file.write(data)
            if not data:
                break
        file.close()
        #print(data)

def deltext():
    list = os.listdir(path=".\\text")
    for text in list:
        os.remove("text\\"+text)
    return list

if __name__ == '__main__':
    HOST, PORT = "127.0.0.1", 1337
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))
    deltext()
    Z = generationKey(server)
    downloadFiles(server)
    #deltext()
    server.close()
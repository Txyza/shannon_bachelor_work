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
        file = open("text/"+str(i)+".txt", "w", encoding="latin-1")
        while True:
            data = server.recv(262144*2).decode("latin-1")
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
            file2 = open("text/" + str(i) + ".txt", "rb")
            text2 = file2.read()
            file2.close()
            #print(text1)
            #a = input()
            #print(text1)
            print(len(text1))
            if fl == 0:
                text1 = xor(text1, text2)
                fl = 1
            else:
                text1 = xor2(text1, text2)
                #print(i, ' -> ', text1)
    return ''.join(text1)


def xorMessage(list, message):
    fl = 0
    for i in range(0, 128):
        if list[i] == 1:
            file2 = open("text/" + str(i) + ".txt", "rb")
            text2 = file2.read()
            file2.close()
            if fl == 0:
                message = xor(message, text2)
                fl = 1
            else:
                message = xor2(message, text2)
    return message


def xor(text1, text2):
    #print('yes')
    lenText2 = len(text2)
    j = 0
    ans = []
    for i in range(len(text1)):
    #for i in text1:
        #print('i -> {}'.format(i))
        #print('text2[j] -> {}'.format(text2[j]))
        #print(i, ' -> ', text2[j])
        #print(chr(i ^ text2[j]))
        #qwe = input()
        ans.append(chr(text1[i] ^ text2[j]))
        #ans.append(chr(i ^ text2[j]))
        #print(ans)
        #ans += chr(ord(i) ^ (ord(text2[j])))
        j+=1
        if j == lenText2-1:
            j = 0
    #print(ans)
    #a = input()

    return ans


def xor2(text1, text2):
    #print('yes')
    lenText2 = len(text2)
    j = 0
    ans = []
    for i in range(len(text1)):
    #for i in text1:
        #print('i -> {}'.format(i))
        #print('text2[j] -> {}'.format(text2[j]))
        #print(i, ' -> ', text2[j])
        #print(chr(i ^ text2[j]))
        #qwe = input()
        text1[i] = chr(ord(text1[i]) ^ text2[j])
        #ans.append(chr(i ^ text2[j]))
        #print(ans)
        #ans += chr(ord(i) ^ (ord(text2[j])))
        j+=1
        if j == lenText2-1:
            j = 0
    #print(ans)
    #a = input()

    return text1


def test():

    call = ['program', '1']


if __name__ == '__main__':
    '''         Получение с сервера тексты и xor '''
    '''
    HOST, PORT = "127.0.0.1", 1337
    #HOST, PORT = "192.168.1.5", 1337
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, PORT))
    Z = generationKey(server)
    #downloadFiles(server)
    server.close()
    '''

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
    for i in range(12, 100):
        HOST, PORT = "127.0.0.1", 1337
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((HOST, PORT))
        Z = generationKey(server)
        ans = bits(Z)
        with open('test/statistic.txt', 'a') as f:
            f.write('{}\n'.format(sum(ans)))
        # downloadFiles(server)
        server.close()
        for name in os.listdir("files/"):
            with open("files/{0}".format(name), "rb") as f:
                text_message = f.read()
            print(text_message)
            #print(text_message[:10])
            #sl = text_message[:10]
            #text_message = text_message[11::]
            text1 = xorTest(text_message, ans)
            with open('test/{0}_{1}.txt'.format(i, name), 'wb') as f:
                for text in text1:
                    f.write(text.encode())
                print("{}_{} encode success".format(i, name))
            with open('test/{0}_{1}.txt'.format(i, name), 'rb') as f:
                for text in text1:
                    text1 = f.read()
            text1 = xorMessage(ans, text1)
            with open('success/{0}_{1}'.format(i, name), 'wb') as f:
                #f.write(sl)
                for text in text1:
                    f.write(text.encode())
                print("{}_{} decode success".format(i, name))
            #print(text1)

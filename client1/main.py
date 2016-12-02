#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==============
#      Date: 01.12.2016
#       Author: Chusovitin Anton Romanovich
# ==============

import socketserver
import random
import time

class Shannon(socketserver.BaseRequestHandler):

    def handle(self):
        self.P = 0;        self.G = 0;        self.Zb = 0
        self.Q = 0
        self.DiffieHellman()
        self.bits()

    def DiffieHellman(self):
        self.Q = random.randint(0, (2 ** 128) - 1)
        while self.miller_rabin(self.Q) == False or self.miller_rabin(2 * self.Q + 1) == False:
            self.Q = random.randint(0, (2**128)-1)
        self.P = 2 * self.Q + 1
        self.G = random.randint(0, (2**128)-1)
        while (self.powmod(self.G, self.Q, self.P) == 1):
            self.G = random.randint(0, (2 ** 128) - 1)
        self.Xa = random.randint(0, (2 ** 128) - 1)
        self.Ya = self.powmod(self.G, self.Xa, self.P)
        self.request.send(str(self.P).encode())
        time.sleep(0.2)
        self.request.send(str(self.G).encode())
        time.sleep(0.2)
        self.request.send(str(self.Ya).encode())
        time.sleep(0.2)
        self.Yb = int(self.request.recv(1024).decode())
        self.Zb = self.powmod(self.Yb, self.Xa, self.P)
        print("Z == ", self.Zb)

    def powmod(self, a, step, mod):
        b = 1
        while step:
            if (step&1) == 1:
                step -= 1
                b = (b * a) % mod
            step >>= 1
            a = (a * a) % mod
        return b % mod


    def miller_rabin(self, n, s=50):
        for j in range(1, s + 1):
            a = random.randint(1, n - 1)
            b = self.Tos(n - 1)
            d = 1
            for i in range(len(b) - 1, -1, -1):
                x = d
                d = (d * d) % n
                if d == 1 and x != 1 and x != n - 1:
                    return True
                if b[i] == 1:
                    d = (d * a) % n
                    if d != 1:
                        return True
                    return False

    def Tos(self, n):
        r = []
        while (n > 0):
            r.append(n % 2)
            n = n / 2
            return r



    def bits(self):
        n = self.Zb
        print("n == ", n)
        ans = []
        sum1 = 0
        for i in range(0,128):
            a = self.bit(n, i)
            if a == 1:
                sum1 += 1
            ans.append(a)
        print(ans)
        print(sum1)
        file = open("statistics_bits128.txt", "a")
        file.write(str(sum1)+"\n")
        file.close()

    def bit(self, num, pos):
        return (num & (1 << pos)) >> pos



if __name__ == '__main__':
    HOST, PORT = "0.0.0.0", 1337
    server = socketserver.TCPServer((HOST, PORT), Shannon)
    server.serve_forever()
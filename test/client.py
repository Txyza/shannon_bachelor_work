import socket
from Lab1.mqv.dh import *
from gmpy2 import *

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect(("127.0.0.1", 8007))


try:
    q = int(conn.recv(2048).decode())
    g = int(conn.recv(2048).decode())
    a1 = int(conn.recv(2048).decode())
    A = int(conn.recv(2048).decode())
except socket.error:
    pass
else:
    b1 = generate_x(q)
    B = gmpy2.powmod(g, b1, q)
    conn.send('{}'.format(b1).encode())
    conn.send('{}'.format(B).encode())
    y = generate_random_p(q)
    Y = gmpy2.powmod(g, y, q)
    conn.send('{}'.format(Y).encode())
    X = int(conn.recv(1024))
    l = 128
    d = 2**l + gmpy2.powmod(X, 1, 2**l)
    e = 2**l + gmpy2.powmod(Y, 1, 2**l)
    Sb = gmpy2.powmod(X * gmpy2.powmod(A, d, q), y + e * b1, q)
    print(Sb)
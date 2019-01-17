import socket
from .dh import *
from gmpy2 import *
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = 8007
s.bind((host, port))
s.listen(3)
while True:
    try:
        client, addr = s.accept()
    except socket.error:
        pass
    else:
        p, b, q = generate_p_b_q()
        g = generate_g(p, b, q)
        client.sendall('{}'.format(q).encode())
        client.sendall('{}'.format(g).encode())
        a1 = generate_x(q)
        A = gmpy2.powmod(g, a1, q)
        client.sendall('{}'.format(a1).encode())
        client.sendall('{}'.format(A).encode())
        x = generate_random_p(q)
        X = gmpy2.powmod(g, x, q)
        l = 128
        client.sendall('{}'.format(X).encode())
        b1 = int(client.recv(1024))
        B = int(client.recv(1024))
        Y = int(client.recv(1024))
        d = 2**l + gmpy2.powmod(X, 1, 2**l)
        e = 2**l + gmpy2.powmod(Y, 1, 2**l)
        Sa = gmpy2.powmod(Y * gmpy2.powmod(B, e, q), x + d * a1, q)
        print('Sa -> ', Sa)

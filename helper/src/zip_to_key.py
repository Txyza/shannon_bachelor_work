import os

list_dir = os.listdir('./../temp')
j = 1
for i in list_dir:
    with open('./../temp/{}'.format(i), 'rb') as f:
        f.seek(2048)
        for count in range(10):
            with open('./../text/{}'.format(j), 'wb') as f2:
                f2.write(f.read(1024))
            j += 1

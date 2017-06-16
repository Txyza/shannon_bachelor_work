import os
import subprocess


def result_book_stack():
    for name in os.listdir("test/"):
        #print(name)
        if name.find('jpg') != -1:
            #print('jpg')
            f = open('result_jpg', 'a')
        elif name.find('cpp') != -1:
            f = open('result_cpp', 'a')
        else:
            f = open('result_bin', 'a')
        call = ['test/bs', '-f',
                'test/{}'.format(name),
                '-w', '8', '-u', '32', '-q']
        data = subprocess.check_output(call)
        #print(name, ' ' ,data)
        f.write('{} = {}'.format(name, data.decode()))
        f.close()


result_book_stack()
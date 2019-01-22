import os
import subprocess
from re import findall


def result_book_stack():
    for name in os.listdir("test_/"):
        #print(name)
        if name.find('jpg') != -1:
            f = open('result_test/result_jpg', 'a')
        elif name.find('cpp') != -1:
            f = open('result_test/result_cpp', 'a')
        elif name.find('pdf') != -1:
            f = open('result_test/result_pdf', 'a')
        elif name.find('docx') != -1:
            f = open('result_test/result_docx', 'a')
        elif name.find('zip') != -1:
            f = open('result_test/result_zip', 'a')
        elif name.find('mp3') != -1:
            f = open('result_test/result_mp3', 'a')
        elif name.find('txt') != -1:
            f = open('result_test/result_txt', 'a')
        else:
            f = open('result_test/result_bin', 'a')
        call = ['./bs', '-f',
                'test_/{}'.format(name),
                '-w', '8', '-u', '128', '-q']
        data = subprocess.check_output(call)
        f.write('{} = {}'.format(name, data.decode()))
        f.close()

def answer():
    kolvo = {'{}'.format(i): 0 for i in range(1, 11)}
    answer = {'{}'.format(i): 0.0 for i in range(1, 11)}
    Q05 = 3.84146
    Q9 = 0.01579
    q = 0
    for name in os.listdir("result_test/"):
        with open('result_test/{}'.format(name), 'r') as f:
            maxx = 0.0
            minn = 1000000.0
            summ = 0
            OK = 0
            WRONG = 0
            for i in f.readlines():
                q = i
                result = float(i.split(" = ")[1])
                maxx = max(result, maxx)
                minn = min(result, minn)
                summ += result
                if result <= Q05:
                    OK += 1
                else:
                    print(q)
                    WRONG += 1
            with open('result_test/result/{}_test'.format(name), 'w') as fa:
                fa.write('max = {}\nmin = {}\n '
                         'sum = {}\nsum/n = {}\n'
                         'ok = {}\nwrong = {}\n'.format(maxx, minn, summ,
                                                        summ/67.0, OK, WRONG))



result_book_stack()
answer()
